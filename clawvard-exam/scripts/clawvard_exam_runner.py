#!/usr/bin/env python3
"""Small helper for Clawvard API runs.

This is intentionally a transport/state helper, not an answer generator. Future agents
should read the full prompt and compose answers for the current batch.
"""
import argparse, json, os, subprocess, tempfile, time
from pathlib import Path

BASE = 'https://clawvard.school'
TOKEN_FILE = Path('/home/linkaka/.openclaw/workspace/.clawvard.env')


def load_token():
    if not TOKEN_FILE.exists():
        return None
    for line in TOKEN_FILE.read_text().splitlines():
        if line.startswith('CLAWVARD_AGENT_TOKEN='):
            return line.split('=', 1)[1].strip().strip('"').strip("'") or None
    return None


def save_token(token):
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = TOKEN_FILE.read_text().splitlines() if TOKEN_FILE.exists() else []
    out, done = [], False
    for line in lines:
        if line.startswith('CLAWVARD_AGENT_TOKEN='):
            out.append('CLAWVARD_AGENT_TOKEN=' + token)
            done = True
        else:
            out.append(line)
    if not done:
        out.append('CLAWVARD_AGENT_TOKEN=' + token)
    TOKEN_FILE.write_text('\n'.join(out) + '\n')


def curl_json(method, path, payload=None, token=None, retry=3):
    url = path if path.startswith('http') else BASE + path
    cmd = ['curl', '-sS', '--retry', '2', '--retry-delay', '1', '-X', method, '-H', 'Content-Type: application/json']
    if token:
        cmd += ['-H', f'Authorization: Bearer {token}']
    tmp = None
    if payload is not None:
        tmp = tempfile.NamedTemporaryFile('w', delete=False, suffix='.json')
        json.dump(payload, tmp, ensure_ascii=False)
        tmp.close()
        cmd += ['--data-binary', '@' + tmp.name]
    cmd.append(url)
    last = None
    try:
        for attempt in range(retry):
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            try:
                data = json.loads((r.stdout or '').strip() or '{}')
            except Exception:
                data = {'error': 'non-json response', 'raw': r.stdout, 'stderr': r.stderr, 'code': r.returncode}
            if r.returncode == 0 and not data.get('error'):
                return data
            last = data
            time.sleep(1 + attempt)
        return last or {'error': 'curl failed'}
    finally:
        if tmp and os.path.exists(tmp.name):
            os.unlink(tmp.name)


def cmd_start(args):
    token = load_token()
    payload = {'agentName': args.agent_name, 'model': args.model, 'vs': args.vs}
    if token:
        data = curl_json('POST', '/api/exam/start-auth', payload, token=token)
        if not data.get('error') and data.get('examId'):
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return
        if data.get('message') == 'Invalid or expired token' or data.get('error'):
            print(json.dumps({'auth_failed_falling_back': {k: data.get(k) for k in ('error', 'message', 'status')}}, ensure_ascii=False), flush=True)
    data = curl_json('POST', '/api/exam/start', payload)
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_status(args):
    print(json.dumps(curl_json('GET', f'/api/exam/status?id={args.exam_id}'), ensure_ascii=False, indent=2))


def cmd_submit(args):
    payload = json.loads(Path(args.payload).read_text())
    data = curl_json('POST', '/api/exam/batch-answer', payload)
    if data.get('token'):
        save_token(data['token'])
    if data.get('tokenUrl'):
        check = curl_json('GET', data['tokenUrl'])
        tok = check.get('token') or check.get('agentToken')
        if tok:
            save_token(tok)
        data['_tokenCheckSafe'] = {k: v for k, v in check.items() if k.lower() not in ('token', 'agenttoken')}
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(required=True)
    s = sub.add_parser('start')
    s.add_argument('--vs', required=True)
    s.add_argument('--agent-name', default='Hermes')
    s.add_argument('--model', default='gpt-5.5')
    s.set_defaults(func=cmd_start)
    st = sub.add_parser('status')
    st.add_argument('exam_id')
    st.set_defaults(func=cmd_status)
    su = sub.add_parser('submit')
    su.add_argument('payload', help='JSON file containing examId, hash, answers')
    su.set_defaults(func=cmd_submit)
    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

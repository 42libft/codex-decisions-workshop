# Decisions API workshop demo

イベントメモを一度の Decisions API 呼び出しで判定する、小さな Python 3 デモです。標準ライブラリだけを使います。

- `predicate`: 実行できる次の行動が書かれているか
- `choice`: 実験・質問・共有・その他のどれか
- `score`: 着手準備が「アイデア」「作業指定」「検証可能」のどの段階か

## 実行

```sh
python3 decisions_demo.py --sample
python3 decisions_demo.py --text '今日の発表をチームに共有する'
python3 decisions_demo.py --text 'この写真のメモを分類して' --image note.png
python3 decisions_demo.py --sample --dry-run
```

`--file memo.txt` で UTF-8 のファイルも入力できます。実行時は `OPENAI_API_KEY` 環境変数、またはリポジトリ直下の `.env.local` を読みます。これらの秘密値は Git に含めません。入力は OpenAI API に送信されるので、ワークショップでは架空のデータを使います。

## Codex Cloud の環境準備

このリポジトリを GitHub に置いた後、Codex Cloud でこのリポジトリを選んで環境を作成します。追加のパッケージは不要です。準備時の確認コマンドは次の2つです。

```sh
python3 -m py_compile decisions_demo.py
python3 decisions_demo.py --sample --dry-run
```

実 API の確認には、環境に `OPENAI_API_KEY` を渡し、`api.openai.com` への HTTPS 通信を許可します。共有環境では各メンバーが自分のキーを Personal vault から渡せるよう、共有の秘密値としてキーを設定しない運用が適しています。公開やメンバー共有の範囲は、環境の設定で別途確認します。

仕様: [OpenAI Decisions API](https://developers.openai.com/api/docs/guides/decisions) ／ [Codex Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)。

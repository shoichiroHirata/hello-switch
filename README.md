# hello-switch

SwitchBot API を使って、家の家電(SwitchBot ハブ経由の赤外線リモコン)を Python で操作するプロジェクトです。

## 目標

- **最終目標:** 長崎市の最低気温を外部から取得し、明け方に自動でエアコンを操作する
  - 実行する条件(何度以下で、何時に、暖房か冷房か)は未定
- **将来:** アプリから家電を操作できるようにする(アプリの種類は未定)

## 機能

| 機能 | 状態 |
|---|---|
| デバイス一覧の取得(API v1.1、署名付き) | ✅ 完了(`devices.py`) |
| ライトの ON/OFF | 未着手 |
| シーンの実行 | Postman で動作確認済み、Python は未着手 |
| 長崎市の最低気温の取得 | 未着手 |
| 気温に応じたエアコンの自動操作 | 未着手 |
| GitHub Actions による定期実行 | 未着手 |
| アプリからの操作 | 未着手 |

## 技術スタック

| 役割 | 使うもの |
|---|---|
| 言語 | Python 3.13 |
| 環境管理 | venv + pip(`requirements.txt`) |
| HTTP 通信 | requests |
| キー管理(ローカル) | python-dotenv(`.env`) |
| キー管理(自動実行) | GitHub Secrets |
| SwitchBot API | v1.1(トークン + シークレットによる HMAC-SHA256 署名) |
| 天気データ | Open-Meteo(無料、API キー不要) |
| 自動実行 | GitHub Actions(定期実行) |
| API の動作確認 | Postman |
| バージョン管理 | Git / GitHub(public リポジトリ) |

## ディレクトリ構成

```
hello-switch/
├── devices.py         # デバイス一覧を表示する
├── requirements.txt   # 使うライブラリの一覧
├── .env.example       # .env のひな形
├── .env               # トークン・シークレット(Git 管理外)
├── .venv/             # Python 仮想環境(Git 管理外)
├── .postman/          # Postman ワークスペースの設定
└── postman/           # Postman のコレクションなど
    └── environments/  # Postman の環境変数(Git 管理外)
```

## セットアップ

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # .env にトークンとシークレットを書く
python devices.py
```

トークンとシークレットは、SwitchBot アプリの「プロフィール → 設定 → アプリバージョンを10回タップ → 開発者向けオプション」で確認できます。

## 秘密情報の扱い

このリポジトリは **public** です。次のものはコミットしないでください。

- トークン、シークレット:`.env` に置きます
- `deviceId`、`sceneId`:コードに直接書かず、`.env` などに置きます
- Postman の環境変数:`postman/environments/` は `.gitignore` で除外しています

コミットする前に `git diff --staged` で中身を確認します。

## SwitchBot API メモ

- ベース URL:`https://api.switch-bot.com/v1.1`
- 認証ヘッダー:`Authorization`(トークン)、`sign`、`t`(ミリ秒の時刻)、`nonce`(ランダムな文字列)
- 署名:`token + t + nonce` を、シークレットを鍵にして HMAC-SHA256 で計算し、Base64 にしたもの
- 成功すると `statusCode: 100` が返る

| 操作 | エンドポイント |
|---|---|
| デバイス一覧 | `GET /devices` |
| シーン一覧 | `GET /scenes` |
| シーン実行 | `POST /scenes/{sceneId}/execute` |
| デバイス操作 | `POST /devices/{deviceId}/commands` |

デバイス操作の Body の例:

```json
{ "command": "turnOn", "parameter": "default", "commandType": "command" }
```

ボタンを自分で学習させたリモコン(`DIY` 系や `Others`)の場合は、`"commandType": "customize"` にして、`command` にアプリでのボタン名を入れます。

赤外線リモコンは信号を送るだけなので、家電が実際に動いたかどうか(状態)は API で取得できません。

## 進め方(ロードマップ)

1. ✅ GitHub にリポジトリを作る
2. ✅ venv を準備し、Python から API v1.1 を呼ぶ
3. ライトの ON/OFF とシーンの実行を Python で行う
4. コードを整理する(共通の処理を関数やモジュールにまとめる)
5. Open-Meteo から長崎市の最低気温を取得する
6. 気温に応じてエアコンを操作する判定を作る
7. GitHub Actions で毎朝自動実行する
8. アプリから操作できるようにする

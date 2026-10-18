# hello-switch

SwitchBot API を使って、SwitchBot ハブに登録した赤外線リモコン家電を Python から操作するツールです。

毎朝 4:00(JST)に長崎市の最低気温の予報を取得し、10℃以下であればエアコンを ON にします。

## 機能

| 機能 | スクリプト |
|---|---|
| デバイス一覧の表示 | `devices.py` |
| シーンの実行 | `scene.py` |
| ライトの ON/OFF | `light.py` |
| 長崎市の今日の最低気温の取得 | `weather.py` |
| 最低気温に応じたエアコンの自動 ON | `auto_aircon.py` |
| 毎朝の定期実行 | `.github/workflows/auto-aircon.yml` |

## 仕様

### エアコンの自動 ON

```
GitHub Actions(毎朝 4:00 JST)
  → Open-Meteo で長崎市の今日の最低気温を取得
  → しきい値以下なら SwitchBot API に turnOn を送信
  → SwitchBot ハブ → 赤外線 → エアコン ON
```

| 項目 | 値 |
|---|---|
| 実行時刻 | 毎日 19:00 UTC(= 4:00 JST) |
| 対象地点 | 長崎市(緯度 32.75、経度 129.88) |
| 判定に使う値 | 当日の最低気温の予報(`temperature_2m_min`) |
| しきい値 | 10℃(環境変数 `AIRCON_THRESHOLD` で変更可) |
| 条件 | 最低気温 ≤ しきい値 のとき ON |
| 運転モード | エアコン側で設定済みのモード(自動)のまま ON |

- GitHub Actions の定期実行は、混雑時に数分〜十数分遅れることがあります
- 赤外線リモコンは信号を送信するだけなので、家電が実際に動作したかどうかは取得できません

### 認証情報

トークンやデバイス ID はリポジトリに含めず、ローカルでは `.env`、GitHub Actions では Secrets から環境変数として読み込みます。

| 環境変数 | 内容 | 使うスクリプト |
|---|---|---|
| `SWITCHBOT_TOKEN` | SwitchBot のトークン | すべて |
| `SWITCHBOT_SECRET` | SwitchBot のシークレット | すべて |
| `SWITCHBOT_SCENE_ID` | 実行するシーンの ID | `scene.py` |
| `SWITCHBOT_LIGHT_ID` | ライトの deviceId | `light.py` |
| `SWITCHBOT_AIRCON_ID` | エアコンの deviceId | `auto_aircon.py` |
| `AIRCON_THRESHOLD` | しきい値(℃)。未設定なら10 | `auto_aircon.py` |

## セットアップ

### 必要なもの

- Python 3.13
- SwitchBot ハブと、ハブに登録した赤外線リモコン家電
- SwitchBot のトークンとシークレット(SwitchBot アプリの「プロフィール → 設定 → アプリバージョンを10回タップ → 開発者向けオプション」で取得)

### インストール

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env` に上の表の値を設定します。deviceId は `python devices.py` で確認できます。

### GitHub Actions の設定

リポジトリの Secrets に、次の3つを登録します。

```
gh secret set SWITCHBOT_TOKEN
gh secret set SWITCHBOT_SECRET
gh secret set SWITCHBOT_AIRCON_ID
```

## 使い方

### ローカル

```
python devices.py        # デバイス一覧(deviceId・名前・種類)を表示
python scene.py          # シーンを実行
python light.py on       # ライトを ON
python light.py off      # ライトを OFF
python weather.py        # 長崎市の今日の最低気温を表示
python auto_aircon.py    # 最低気温がしきい値以下ならエアコンを ON
```

しきい値を変えて実行する場合:

```
AIRCON_THRESHOLD=30 python auto_aircon.py
```

### GitHub Actions

定期実行は自動で行われます。手動で実行する場合は、`threshold` でしきい値を指定できます(省略時は10℃)。

```
gh workflow run auto-aircon.yml -f threshold=30
gh run view --log
```

GitHub の Actions タブにある **Run workflow** からも実行できます。

## 技術スタック

| 役割 | 技術 |
|---|---|
| 言語 | Python 3.13 |
| 環境管理 | venv、pip(`requirements.txt`) |
| HTTP 通信 | requests |
| 設定の読み込み | python-dotenv |
| 署名の生成 | hmac、hashlib、base64(標準ライブラリ) |
| 家電の操作 | SwitchBot API v1.1 |
| 天気データ | Open-Meteo Forecast API |
| 定期実行 | GitHub Actions |
| 認証情報の管理 | `.env`(ローカル)、GitHub Secrets(Actions) |
| API の動作確認 | Postman |

## ディレクトリ構成

```
hello-switch/
├── switchbot_api.py     # SwitchBot API の共通処理(署名付きヘッダーの作成、コマンド送信)
├── devices.py           # デバイス一覧を表示
├── scene.py             # シーンを実行
├── light.py             # ライトを ON/OFF
├── weather.py           # 長崎市の今日の最低気温を取得
├── auto_aircon.py       # 最低気温がしきい値以下ならエアコンを ON
├── requirements.txt     # 依存ライブラリ
├── .env.example         # 環境変数のひな形
├── .github/workflows/
│   └── auto-aircon.yml  # 毎朝 4:00 JST に auto_aircon.py を実行
├── .postman/            # Postman ワークスペースの設定
└── postman/             # Postman のコレクションなど
```

## 外部 API

### SwitchBot API v1.1

- ベース URL:`https://api.switch-bot.com/v1.1`
- 認証:リクエストごとに `Authorization`(トークン)、`t`(ミリ秒の UNIX 時刻)、`nonce`(UUID)、`sign` をヘッダーに付けます。`sign` は `token + t + nonce` をシークレットで HMAC-SHA256 署名し、Base64 エンコードした値です
- 成功時のレスポンスは `statusCode: 100` です

| 操作 | エンドポイント |
|---|---|
| デバイス一覧 | `GET /devices` |
| シーン一覧 | `GET /scenes` |
| シーン実行 | `POST /scenes/{sceneId}/execute` |
| デバイス操作 | `POST /devices/{deviceId}/commands` |

デバイス操作のリクエストボディ:

```json
{ "command": "turnOn", "parameter": "default", "commandType": "command" }
```

### Open-Meteo Forecast API

```
GET https://api.open-meteo.com/v1/forecast?latitude=32.75&longitude=129.88&daily=temperature_2m_min&timezone=Asia/Tokyo&forecast_days=1
```

`daily.temperature_2m_min[0]` を当日の最低気温(℃)として使います。API キーは不要です。

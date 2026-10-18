# hello-switch

SwitchBot API を使って、家の家電(SwitchBot ハブ経由の赤外線リモコン)を Python で操作するプロジェクトです。

毎朝4時に長崎市の最低気温を調べ、**10℃以下ならエアコンを自動で ON** にします。

## 機能

| 機能 | ファイル | 状態 |
|---|---|---|
| デバイス一覧の取得 | `devices.py` | ✅ |
| シーンの実行 | `scene.py` | ✅ |
| ライトの ON/OFF | `light.py` | ✅ |
| 長崎市の最低気温の取得 | `weather.py` | ✅ |
| 最低気温が10℃以下ならエアコンを ON | `auto_aircon.py` | ✅ |
| 毎朝4時の自動実行 | `.github/workflows/auto-aircon.yml` | ✅ |
| アプリからの操作 | | 未着手 |

## しくみ

```
GitHub Actions(毎朝 4:00 JST)
  → Open-Meteo で長崎市の今日の最低気温を取得
  → 10℃以下なら
  → SwitchBot API v1.1(署名付き)で turnOn を送る
  → ハブ → 赤外線 → エアコン ON
```

エアコンは、あらかじめ設定した自動モードで ON になります。

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
| バージョン管理 | Git / GitHub(public リポジトリ、GitHub Flow) |

## ディレクトリ構成

```
hello-switch/
├── switchbot_api.py   # 共通処理: 署名付きヘッダーの作成(make_headers)、コマンド送信(send_command)
├── devices.py         # デバイス一覧を表示する
├── scene.py           # シーンを実行する
├── light.py           # ライトを ON/OFF する
├── weather.py         # 長崎市の今日の最低気温を取得する(get_min_temperature)
├── auto_aircon.py     # 最低気温が10℃以下ならエアコンを ON にする
├── requirements.txt   # 使うライブラリの一覧
├── .env.example       # .env のひな形
├── .env               # トークンや ID(Git 管理外)
├── .venv/             # Python 仮想環境(Git 管理外)
├── .github/workflows/
│   └── auto-aircon.yml  # 毎朝4時に auto_aircon.py を実行する
├── .postman/          # Postman ワークスペースの設定
└── postman/           # Postman のコレクションなど
    └── environments/  # Postman の環境変数(Git 管理外)
```

## セットアップ(ローカル)

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env` に次の値を書きます。

| 変数 | 内容 |
|---|---|
| `SWITCHBOT_TOKEN` | SwitchBot のトークン |
| `SWITCHBOT_SECRET` | SwitchBot のシークレット |
| `SWITCHBOT_SCENE_ID` | `scene.py` で実行するシーンの ID |
| `SWITCHBOT_LIGHT_ID` | ライトの deviceId |
| `SWITCHBOT_AIRCON_ID` | エアコンの deviceId |

- トークンとシークレットは、SwitchBot アプリの「プロフィール → 設定 → アプリバージョンを10回タップ → 開発者向けオプション」で確認できます
- deviceId は `python devices.py` で、シーンの ID は `GET /v1.1/scenes` で確認できます

## 使い方(ローカル)

```
python devices.py        # デバイス一覧(deviceId・名前・種類)
python scene.py          # シーンを実行
python light.py on       # ライトを ON
python light.py off      # ライトを OFF
python weather.py        # 長崎市の今日の最低気温を表示
python auto_aircon.py    # 最低気温が10℃以下ならエアコンを ON
```

しきい値を一時的に変えて試すこともできます(そのコマンドの間だけ有効)。

```
AIRCON_THRESHOLD=30 python auto_aircon.py
```

`(.venv)` がプロンプトに表示されていないときは、先に `source .venv/bin/activate` を実行してください。

## 自動実行(GitHub Actions)

### Secrets の登録

```
gh secret set SWITCHBOT_TOKEN
gh secret set SWITCHBOT_SECRET
gh secret set SWITCHBOT_AIRCON_ID
gh secret list
```

値はコマンドに直接書かず、聞かれてから入力します(ターミナルの履歴に残さないため)。

### 実行タイミング

- 毎日 19:00 UTC(= 4:00 JST)。cron の時刻は UTC で書きます
- 混雑していると、数分〜十数分遅れることがあります
- public リポジトリは、60日間コミットがないと定期実行が止まります。止まったら Actions タブから再開します

### 手動でテストする

しきい値を指定して手動実行できます。指定しない場合は10℃です。

```
gh workflow run auto-aircon.yml -f threshold=30
gh run list
gh run view --log
```

ブラウザの Actions タブにある **Run workflow** ボタンからも実行できます。

## 開発の流れ(GitHub Flow)

`main` には直接コミットせず、作業ごとにブランチを切ります。

```
git switch main
git pull
git switch -c feature/xxx      # docs/xxx、fix/xxx など
# 作業してコミット
git push -u origin feature/xxx
gh pr create --fill
gh pr merge --merge --delete-branch
git switch main
git pull
git fetch --prune
```

## 秘密情報の扱い

このリポジトリは **public** です。次のものはコミットしないでください。

- トークン、シークレット、deviceId、sceneId:`.env`(ローカル)と GitHub Secrets(Actions)に置きます
- Postman の環境変数:`postman/environments/` は `.gitignore` で除外しています

あわせて、次のことにも気をつけてください。

- コミットする前に、`git diff --staged` で中身を確認します
- Actions のログは誰でも見られます。Secrets の値は `***` に伏せられますが、`print` した ID やトークンはそのまま表示されます

## SwitchBot API メモ

- ベース URL:`https://api.switch-bot.com/v1.1`
- 認証ヘッダー:`Authorization`(トークン)、`sign`、`t`(ミリ秒の時刻)、`nonce`(ランダムな文字列)
- 署名:`token + t + nonce` を、シークレットを鍵にして HMAC-SHA256 で計算し、Base64 にしたもの。リクエストのたびに作り直します
- 成功すると `statusCode: 100` が返ります

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

## Open-Meteo メモ

```
GET https://api.open-meteo.com/v1/forecast?latitude=32.75&longitude=129.88&daily=temperature_2m_min&timezone=Asia/Tokyo&forecast_days=1
```

`daily.temperature_2m_min[0]` が今日の最低気温(℃)です。

## ロードマップ

1. ✅ GitHub にリポジトリを作る
2. ✅ venv を準備し、Python から API v1.1 を呼ぶ
3. ✅ ライトの ON/OFF とシーンの実行を Python で行う
4. ✅ 共通処理を `switchbot_api.py` にまとめる
5. ✅ Open-Meteo から長崎市の最低気温を取得する
6. ✅ 最低気温が10℃以下ならエアコンを ON にする
7. ✅ GitHub Actions で毎朝4時に自動実行する
8. アプリから操作できるようにする

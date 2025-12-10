# Nature Remo ダッシュボードガイド

7〜10インチのタブレットディスプレイで管理するための、見やすく分かりやすいダッシュボード設定ガイドです。

## 目次

1. [概要](#概要)
2. [セットアップ方法](#セットアップ方法)
3. [ダッシュボード例](#ダッシュボード例)
4. [センサー属性の活用](#センサー属性の活用)
5. [カスタマイズ方法](#カスタマイズ方法)
6. [推奨設定](#推奨設定)

## 概要

このNature Remo統合は、タブレットディスプレイでの表示を最適化するために、以下の機能を提供します:

### 強化されたセンサー属性

各センサーには、ダッシュボード表示を充実させるための追加属性が含まれています:

#### 温度センサー
- `comfort_level`: 快適度レベル(寒い/少し寒い/快適/やや暑い/暑い)
- `comfort_icon`: 状態に応じたアイコン
- `comfort_color`: 視覚的なカラーコード
- `last_updated`: 最終更新時刻
- `device_serial`: デバイスシリアル番号
- `firmware_version`: ファームウェアバージョン

#### 湿度センサー
- `comfort_level`: 快適度レベル(乾燥/やや乾燥/快適/やや湿気/多湿)
- `comfort_icon`: 状態に応じたアイコン
- `comfort_color`: 視覚的なカラーコード
- `recommendation`: 推奨アクション
- `last_updated`: 最終更新時刻

#### 照度センサー
- `brightness_level`: 明るさレベル(真っ暗/暗い/薄暗い/普通/明るい/非常に明るい)
- `brightness_icon`: 状態に応じたアイコン
- `brightness_color`: 視覚的なカラーコード
- `recommendation`: 推奨アクション
- `last_updated`: 最終更新時刻

#### 電力センサー
- `usage_level`: 使用レベル(低/通常/高/非常に高)
- `usage_icon`: 状態に応じたアイコン
- `usage_color`: 視覚的なカラーコード
- `status`: 現在の状態
- `estimated_daily_cost`: 推定日次コスト(円)
- `estimated_daily_kwh`: 推定日次電力量(kWh)

## セットアップ方法

### 1. ダッシュボードの作成

Home Assistantのサイドバーから:
1. **設定** → **ダッシュボード** を開く
2. **ダッシュボードを追加** をクリック
3. **新しいダッシュボード** を選択
4. 名前を入力(例: "Nature Remo Control")
5. **作成** をクリック

### 2. 設定例のインポート

`dashboard_examples` フォルダには、2つの設定例が用意されています:

#### tablet_dashboard.yaml
複数のビューを持つ高機能ダッシュボード。グラフ表示や詳細な制御が可能。

```bash
# ファイルの内容をコピーして、ダッシュボードのYAMLモードに貼り付け
```

#### simple_tablet_dashboard.yaml
カスタムカード不要の、シンプルで使いやすいダッシュボード。すぐに使い始められます。

```bash
# ファイルの内容をコピーして、ダッシュボードのYAMLモードに貼り付け
```

### 3. エンティティIDの調整

設定例では、以下のようなエンティティIDが使用されています:
- `sensor.living_room_temperature`
- `climate.living_room_ac`
- `light.living_room_light`

**あなたの環境に合わせて変更してください**

エンティティIDは、**設定** → **デバイスとサービス** → **エンティティ** で確認できます。

## ダッシュボード例

### レイアウト1: オーバービュー(推奨)

壁掛けタブレットに最適な、一目で状況が分かるレイアウト:

```yaml
# 環境センサー(上部)
- 温度、湿度、照度を横並びで表示
- グラフ付きで推移を確認可能

# エアコン制御(中央)
- サーモスタットカードで直感的に操作
- クイック設定ボタンで素早く設定変更

# 電力モニター(下部)
- ゲージで現在の消費電力を視覚化
- 推移グラフで使用傾向を確認
```

### レイアウト2: コンパクト表示

7インチディスプレイに最適な、シンプルなレイアウト:

```yaml
# すべてのエンティティを縦に並べたシンプルな構成
# スクロールで全体を確認可能
# タップ操作で詳細設定
```

## センサー属性の活用

### テンプレートセンサーの作成

センサー属性を活用して、より分かりやすい表示を作成できます:

```yaml
# configuration.yaml に追加

template:
  - sensor:
      - name: "快適度インジケーター"
        state: "{{ state_attr('sensor.living_room_temperature', 'comfort_level') }}"
        icon: "{{ state_attr('sensor.living_room_temperature', 'comfort_icon') }}"

      - name: "湿度状態"
        state: "{{ state_attr('sensor.living_room_humidity', 'comfort_level') }}"
        icon: "{{ state_attr('sensor.living_room_humidity', 'comfort_icon') }}"
        attributes:
          recommendation: "{{ state_attr('sensor.living_room_humidity', 'recommendation') }}"

      - name: "電力使用状況"
        state: "{{ state_attr('sensor.smart_meter_power', 'usage_level') }}"
        icon: "{{ state_attr('sensor.smart_meter_power', 'usage_icon') }}"
        attributes:
          daily_cost: "{{ state_attr('sensor.smart_meter_power', 'estimated_daily_cost') }}"
```

### Markdown カードでの表示

属性を使って、分かりやすい情報カードを作成:

```yaml
type: markdown
content: |
  ## 室内環境

  **温度**: {{ states('sensor.living_room_temperature') }}°C
  - 状態: {{ state_attr('sensor.living_room_temperature', 'comfort_level') }}

  **湿度**: {{ states('sensor.living_room_humidity') }}%
  - 状態: {{ state_attr('sensor.living_room_humidity', 'comfort_level') }}
  - {{ state_attr('sensor.living_room_humidity', 'recommendation') }}

  **明るさ**: {{ states('sensor.living_room_illuminance') }} lx
  - 状態: {{ state_attr('sensor.living_room_illuminance', 'brightness_level') }}

  {% if states('sensor.smart_meter_power') != 'unavailable' %}
  ## 電力使用状況

  **現在の消費電力**: {{ states('sensor.smart_meter_power') }} W
  - 状態: {{ state_attr('sensor.smart_meter_power', 'status') }}
  - 推定日次コスト: ¥{{ state_attr('sensor.smart_meter_power', 'estimated_daily_cost') }}
  {% endif %}
```

## カスタマイズ方法

### 色とアイコンのカスタマイズ

各センサーの属性には `_color` と `_icon` が含まれており、条件付きカードで活用できます:

```yaml
type: entity
entity: sensor.living_room_temperature
style: |
  :host {
    --paper-item-icon-color: {{ state_attr('sensor.living_room_temperature', 'comfort_color') }};
  }
```

### タブレット向け最適化設定

#### フルスクリーン表示(キオスクモード)

Home Assistant Companion アプリの設定:
1. **設定** → **Companion アプリ** → **ダッシュボード**
2. **キオスクモード** を有効化
3. サイドバーとヘッダーが非表示になります

#### 画面の自動オフを防止

タブレットの設定:
1. **設定** → **ディスプレイ**
2. **スリープ** を「なし」に設定
3. または **常時表示** を有効化

#### 明るさの自動調整

照度センサーを使用した自動化:

```yaml
# automations.yaml

- alias: "タブレット輝度自動調整"
  trigger:
    - platform: state
      entity_id: sensor.living_room_illuminance
  action:
    - choose:
        - conditions:
            - condition: numeric_state
              entity_id: sensor.living_room_illuminance
              below: 50
          sequence:
            - service: light.turn_on
              target:
                entity_id: light.tablet_screen  # タブレットの画面輝度制御
              data:
                brightness: 50
        - conditions:
            - condition: numeric_state
              entity_id: sensor.living_room_illuminance
              above: 500
          sequence:
            - service: light.turn_on
              target:
                entity_id: light.tablet_screen
              data:
                brightness: 255
```

## 推奨設定

### 7インチタブレット向け

- **レイアウト**: シンプルなエンティティリスト形式
- **カラム数**: 2列まで
- **フォントサイズ**: 中〜大
- **カード**: 基本的なエンティティカード、ボタンカード

### 10インチタブレット向け

- **レイアウト**: グリッド形式、複数セクション
- **カラム数**: 3〜4列
- **フォントサイズ**: 標準
- **カード**: グラフカード、ゲージカード、サーモスタットカード

### 壁掛けディスプレイ向け

- **更新間隔**: 30秒〜1分
- **アニメーション**: 有効(視認性向上)
- **通知**: 音声通知オフ、視覚的通知のみ
- **キオスクモード**: 有効

## スクリプト例

よく使う操作をスクリプト化:

```yaml
# scripts.yaml

ac_comfort_mode:
  alias: "快適モード"
  sequence:
    - choose:
        # 夏季(温度が高い場合)
        - conditions:
            - condition: numeric_state
              entity_id: sensor.living_room_temperature
              above: 26
          sequence:
            - service: climate.set_temperature
              target:
                entity_id: climate.living_room_ac
              data:
                temperature: 24
                hvac_mode: cool
        # 冬季(温度が低い場合)
        - conditions:
            - condition: numeric_state
              entity_id: sensor.living_room_temperature
              below: 20
          sequence:
            - service: climate.set_temperature
              target:
                entity_id: climate.living_room_ac
              data:
                temperature: 22
                hvac_mode: heat
        # 適温の場合
      default:
        - service: climate.turn_off
          target:
            entity_id: climate.living_room_ac

humidity_control:
  alias: "湿度調整"
  sequence:
    - choose:
        # 乾燥している場合
        - conditions:
            - condition: numeric_state
              entity_id: sensor.living_room_humidity
              below: 40
          sequence:
            - service: notify.mobile_app
              data:
                message: "湿度が低いです。加湿器の使用を推奨します。"
        # 湿気が多い場合
        - conditions:
            - condition: numeric_state
              entity_id: sensor.living_room_humidity
              above: 65
          sequence:
            - service: climate.set_hvac_mode
              target:
                entity_id: climate.living_room_ac
              data:
                hvac_mode: dry
```

## トラブルシューティング

### センサーが表示されない

1. **設定** → **デバイスとサービス** でNature Remo統合を確認
2. デバイスが正しく認識されているか確認
3. 統合を再読み込み

### 属性が表示されない

1. Home Assistantを再起動
2. 統合が最新バージョンか確認
3. センサーの状態が `unknown` または `unavailable` でないか確認

### ダッシュボードが重い

1. グラフカードの履歴期間を短縮(24時間→12時間)
2. 更新間隔を長く設定
3. 不要なカードを削除

## 参考リンク

- [Home Assistant Dashboard Documentation](https://www.home-assistant.io/dashboards/)
- [Nature Remo Cloud API](https://developer.nature.global/)
- [カード一覧](https://www.home-assistant.io/dashboards/cards/)

## サポート

問題や機能要望は、GitHubのIssueで報告してください:
https://github.com/98kuwa036/codings/issues

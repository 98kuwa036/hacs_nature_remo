# ダッシュボード例

7〜10インチのタブレットディスプレイでNature Remoを管理するための、ダッシュボード設定例を提供します。

## 📁 ファイル一覧

### 1. `tablet_dashboard.yaml`
**複数ビュー対応の高機能ダッシュボード**

- **概要ビュー**: 環境センサー、エアコン制御、電力モニター
- **詳細制御ビュー**: すべてのデバイスの詳細設定
- **センサービュー**: グラフを使用した履歴表示
- **ステータスビュー**: 壁掛けタブレット向けのコンパクト表示

**対象**:
- 10インチタブレット
- 機能を使いこなしたい方
- グラフ表示が必要な方

**必要なカスタムカード**:
- `mini-graph-card` (グラフ表示用)

### 2. `simple_tablet_dashboard.yaml`
**シンプルで使いやすい基本ダッシュボード**

- カスタムカード不要
- 1ページで全機能にアクセス
- 縦スクロールで全体を確認

**対象**:
- 7インチタブレット
- シンプルな操作を好む方
- すぐに使い始めたい方

**必要なカスタムカード**:
- なし(標準機能のみ)

### 3. `card_templates.yaml`
**カスタムカードのテンプレート集**

以下のカードテンプレートが含まれています:

1. **environment_monitor_card** - 環境モニターカード
2. **simple_environment_card** - シンプル環境カード
3. **ac_control_card** - エアコンコントロールカード
4. **power_monitor_card** - 電力モニターカード
5. **simple_power_card** - シンプル電力カード
6. **unified_control_panel** - 統合コントロールパネル
7. **tablet_fullscreen_dashboard** - タブレット向けフルスクリーン
8. **minimal_status_card** - ミニマルステータスカード

**対象**:
- カスタマイズしたい方
- 部分的に機能を追加したい方

## 🚀 クイックスタート

### ステップ1: ファイルを選ぶ

あなたのタブレットサイズと用途に合わせて選択:

| タブレット | 用途 | おすすめファイル |
|----------|------|----------------|
| 7インチ | シンプルに使いたい | `simple_tablet_dashboard.yaml` |
| 10インチ | 詳細な制御が必要 | `tablet_dashboard.yaml` |
| どちらでも | 部分的にカスタマイズ | `card_templates.yaml` |

### ステップ2: ダッシュボードを作成

1. Home Assistantにログイン
2. サイドバーから任意のダッシュボードを開く
3. 右上の **︙** → **ダッシュボードを編集**
4. または、新しいダッシュボードを作成

### ステップ3: YAMLをコピー

#### 全体のダッシュボードを作成する場合:

1. ダッシュボード画面で右上の **︙** → **未加工の設定エディター**
2. 選択したファイル(`tablet_dashboard.yaml` または `simple_tablet_dashboard.yaml`)の内容をコピー
3. エディターに貼り付け
4. **保存**

#### 個別のカードを追加する場合:

1. ダッシュボード編集モードで **カードを追加**
2. 一番下までスクロールして **手動** を選択
3. `card_templates.yaml` から必要なカードテンプレートをコピー
4. 貼り付けて **保存**

### ステップ4: エンティティIDを変更

設定例では以下のようなエンティティIDが使用されています:

```yaml
sensor.living_room_temperature    # あなたの温度センサーに変更
climate.living_room_ac           # あなたのエアコンに変更
light.living_room_light          # あなたの照明に変更
```

**エンティティIDの確認方法**:
1. **設定** → **デバイスとサービス**
2. Nature Remo統合をクリック
3. デバイスをクリック
4. 各エンティティのIDを確認

### ステップ5: 保存して確認

1. **保存** をクリック
2. 編集モードを終了
3. ダッシュボードが表示されることを確認

## 📱 タブレット設定

### キオスクモード(全画面表示)

#### Home Assistant Companionアプリ(Android/iOS)

1. アプリの **設定**
2. **Companion アプリ** → **ダッシュボード**
3. **キオスクモード** を有効化

#### ブラウザ(Fully Kiosk Browser等)

1. Fully Kiosk Browserをインストール
2. Home AssistantのURLを設定
3. **キオスクモード** を有効化
4. **画面を常にオン** に設定

### 画面の明るさ自動調整

Nature Remoの照度センサーを使用して、タブレットの明るさを自動調整できます。

`DASHBOARD_GUIDE.md` の「明るさの自動調整」セクションを参照してください。

## 🎨 カスタマイズ

### 色の変更

カードのスタイルをカスタマイズ:

```yaml
style: |
  ha-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
```

### アイコンの変更

MDI(Material Design Icons)から選択:

```yaml
icon: mdi:air-conditioner  # エアコン
icon: mdi:lightbulb        # 電球
icon: mdi:thermometer      # 温度計
```

アイコン一覧: https://pictogrammers.com/library/mdi/

### フォントサイズの変更

```yaml
style: |
  ha-card {
    font-size: 1.5em;  # 1.5倍のサイズ
  }
```

## 🔧 トラブルシューティング

### カードが表示されない

- YAMLの構文エラーを確認
- エンティティIDが正しいか確認
- カスタムカードが必要な場合、インストールされているか確認

### カスタムカードのインストール

**HACS経由でインストール**:

1. HACSを開く
2. **フロントエンド** をクリック
3. 右下の **︙** → **カスタムリポジトリ**
4. 必要なカードのリポジトリURLを追加:
   - Mini Graph Card: `kalkih/mini-graph-card`
   - Template Entity Row: `thomasloven/lovelace-template-entity-row`

### エンティティが見つからない

1. **設定** → **デバイスとサービス** でNature Remo統合を確認
2. デバイスが正しく検出されているか確認
3. 統合を再読み込み

## 💡 おすすめの使い方

### 壁掛けタブレット

- `simple_tablet_dashboard.yaml` を使用
- キオスクモードを有効化
- 画面を常時オンに設定
- 照度センサーで明るさ自動調整

### デスクトップ タブレット

- `tablet_dashboard.yaml` を使用
- 複数のビューで情報を整理
- グラフで履歴を確認

### モバイル兼用

- `card_templates.yaml` から必要なカードのみ使用
- レスポンシブデザインで自動調整

## 📚 詳細ドキュメント

より詳しい情報は、以下のドキュメントを参照してください:

- **[DASHBOARD_GUIDE.md](../DASHBOARD_GUIDE.md)** - 完全なダッシュボードガイド
- **[README.md](../README.md)** - 統合の基本情報

## 🆘 サポート

問題が発生した場合や、機能要望がある場合は、GitHubのIssueで報告してください:

https://github.com/98kuwa036/codings/issues

## 📝 ライセンス

このプロジェクトは、個人利用および教育目的で提供されています。

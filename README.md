# アパレル検索支援サービス
@nao708810

## How to use

1. アプリケーションをローカルにクローンします。

```cmd
git clone https://github.com/nao708810/app-apparel-search
```

2. appsフォルダに移動します。

```cmd
cd apps
```

3. パッケージをインストールします。
   requirements.txt は必要なパッケージを羅列しています。

```cmd
pip install -r requirements.txt
```

4. apps\config.sampleファイルをコピーして、config.pyにリネームします。

5. config.py に必要な情報を設定します。
   Azure ポータルから Custom Vision と Storage Blob リソースを作成する必要があります。

6. アプリケーションを起動します。

```cmd
python manage.py
```
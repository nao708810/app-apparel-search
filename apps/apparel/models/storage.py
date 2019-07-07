"""
Connect Azure Storage
"""
from azure.cosmosdb.table.tableservice import TableService
# from azure.cosmosdb.table.models import Entity

#Azureストレージ操作クラス
class Storage():
    """Azure Storage Table 操作クラス

    Azure Storage Table service を操作するためのクラス。
    config.pyに設定した Azure Storage のアカウント名と接続キーがインスタンスに必要。

    Attributes:
        table_service: TableService クラスのインスタンス

    """
    def __init__(self, name, key):
        #コンストラクタの定義
        self.table_service = TableService(account_name=name, account_key=key)

    #ユーザーIDをキーにストレージ検索
    def userid_search(self, table_name, userid_key):
        """ユーザーIDをキーにストレージ検索、取得

        引数のユーザーIDキーからフィルターワードを生成し、指定したTable名から
        走行データを取得する。

        Args:
            table_name (str): Azure Storage Table 名
            userid_key (str): ユーザーIDの検索キー

        Returns:
            複数の entity オブジェクトのリストである、走行データを返却する。

        """
        filter_keyword = "UserId eq " + "'" +  userid_key + "'"
        run_data = self.table_service.query_entities(table_name, filter=filter_keyword)
        return run_data

    #ストレージエンティティをすべて取得
    def get_storage_all(self, table_name):
        """指定したTableの全ての走行データを取得

        指定したTable名から全ての走行データを取得する。

        Args:
            table_name (str): Azure Storage Table 名

        Returns:
            複数の entity オブジェクトのリストである、走行データを返却する。

        """
        run_data = self.table_service.query_entities(table_name)
        return run_data

    #ストレージエンティティ更新（コメント、タグ、AI分析結果）
    def update_entity(self, table_name, entities):
        """走行データの更新

        引数の走行データで、指定したTable名の走行データを更新する。

        Args:
            table_name (str): Azure Storage Table 名
            entities (list): 走行データのリスト

        """
        for entity in entities:
            self.table_service.update_entity(table_name, entity)

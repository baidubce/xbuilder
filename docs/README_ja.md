<div align="center">
<img src='image/logo.png' alt='logo' width='700' >
<br>

[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.9+-orange.svg)
![Supported OSs](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)
</div>

[简体中文](../README.md) | [English](./README_en.md) | 日本語

<br>


## AppBuilder SDKとは？

Baidu AI Cloud Qianfan AppBuilder SDKは、[Baidu AI Cloud Qianfan AppBuilder](https://appbuilder.cloud.baidu.com/)によって提供されるAIネイティブアプリケーション開発者向けの「ワンストップ開発ツール」です。

Baidu AI Cloud Qianfan AppBuilder-SDKは、AIアプリケーション開発者向けに以下の基本機能を提供します：

1. 利用

    - 大規模言語モデルを利用し、Baidu AI Cloud Qianfan大規模モデルプラットフォームで自由にモデルにアクセスし、プロンプトを開発および最適化します。

    - 機能コンポーネントを統合し、Baiduのエコシステムから提供される40以上の高品質なグループを提供し、エージェントアプリケーションに力を与えます。

    - AIネイティブアプリケーションを統合し、[Baidu AI Cloud Qianfan AppBuilderプラットフォーム](https://console.bce.baidu.com/ai_apaas/app)で公開されたAIネイティブアプリケーションにAppBuilderClientを通じてアクセスおよび管理し、エンドクラウドコンポーネントをリンクするためにローカル関数を登録します。

2. オーケストレーション

    - 知識フローをオーケストレーションおよび管理し、KnowledgeBaseを通じて知識ベースを管理し、文書および知識スライスの作成、読み取り、更新、削除（CRUD）操作を実行し、Baidu AI Cloud Qianfan AppBuilderプラットフォームと共に業界グレードのRAGアプリケーションを開発します。

    - ワークフローをオーケストレーションおよび自動化し、`Message`、`Component`、`FlaskRuntime`、`ChainlitRuntime`などの多層ワークフロー抽象を提供し、ワークフローのオーケストレーションを実現し、LangChainやOpenAIなどの業界エコシステム機能と統合します。

3. 監視
    - 開発者が生産環境で使用するための可視化トレースおよび詳細なデバッグログなどの監視ツールを提供します。

4. デプロイメント

    - FlaskRuntimeは、FlaskおよびGunicornに基づくAPIサービスとしてデプロイメントをサポートします。
    - ChainlitRuntimeは、Chainlitに基づく対話型フロントエンドアプリケーションとしてデプロイメントをサポートします。
    - プログラムをBaidu Cloudに迅速にデプロイし、パブリックネットワークAPIサービスを提供し、AppBuilderのワークフロー機能と統合するためのappbuilder_bce_deployツールを提供します。


## どのようにインストールしますか？

#### Baidu AI Cloud Qianfan AppBuilder SDKの最新バージョンは0.9.8（2024-12-10）です

Baidu AI Cloud Qianfan AppBuilder SDKのリリースノートについては、[バージョン説明](DevelopGuide/ChangeLog/changelog.md)をご覧ください。

- 最新の安定バージョンの`Python`をインストールすることをお勧めします。

```bash
python3 -m pip install --upgrade appbuilder-sdk
```
- `Java`および`Go`バージョンのインストールや`Docker`イメージの使用については、[インストール手順](QuickStart/StartFirstAINativeApplication/install.md)をご覧ください。


## 最初のAIネイティブアプリケーションをすぐに開始しましょう！

- `>=3.9`のPython環境に`appbuilder sdk`をインストールし、このエンドツーエンドアプリケーションの例を使用してください。
- 例では試用トークンが提供されていますが、アクセスとQPSが制限されています。正式な使用には個人のトークンに置き換えてください。

### 1. 大規模言語モデル
- `Playground`コンポーネントは自由に呼び出すことができます。Baidu AI Cloud Qianfanモデルプラットフォームで許可された任意のモデルに対して、プロンプトテンプレートとモデルパラメータをカスタマイズできます。

#### コード例

```python
import appbuilder
import os

# 環境変数にTOKENを設定します。以下のTOKENはアクセスとQPSが制限された試用TOKENです。正式な使用には個人のTOKENに置き換えてください。
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

# プロンプトテンプレートを定義します。
template_str = "あなたは{role}の役割を果たします。私の質問に答えてください。\n\n質問：{question}。\n\n回答："

# 入力を定義し、playgroundコンポーネントを呼び出します。
input = appbuilder.Message({"role": "Javaエンジニア", "question": "Java言語のメモリ回収メカニズムについて簡単に説明してください。100文字以内でお願いします。"})

playground = appbuilder.Playground(prompt_template=template_str, model="Qianfan-Agent-Speed-8K")

# タイプライターのように、ストリーム形式で大規模モデルの回答内容を表示します。
output = playground(input, stream=True, temperature=1e-10)
for stream_message in output.content:
    print(stream_message)

# ストリーム出力が終了した後、再度完全な大規模モデルの対話結果を表示できます。回答内容の他に、トークンの使用量も含まれます。
print(output.model_dump_json(indent=4))

```
#### 回答表示

```shell
Java言語の
メモリ回収メカニズムは、ガベージコレクタ（Garbage Collector）を通じて実現されます。
ガベージコレクタは、使用されなくなったオブジェクトを自動的に検出し、その占有するメモリ空間を解放します。これにより、システムのメモリが枯渇しないようにします。
Javaは、シリアルコレクタ、パラレルコレクタ、CMSコレクタ、G1コレクタなど、さまざまなガベージコレクタを提供しており、異なるシナリオでのパフォーマンス要件に対応しています。

{
    "content": "Java言語のメモリ回収メカニズムは、ガベージコレクタ（Garbage Collector）を通じて実現されます。ガベージコレクタは、使用されなくなったオブジェクトを自動的に検出し、その占有するメモリ空間を解放します。これにより、システムのメモリが枯渇しないようにします。Javaは、シリアルコレクタ、パラレルコレクタ、CMSコレクタ、G1コレクタなど、さまざまなガベージコレクタを提供しており、異なるシナリオでのパフォーマンス要件に対応しています。",
    "name": "msg",
    "mtype": "dict",
    "id": "2bbee989-40e3-45e4-9802-e144cdc829a9",
    "extra": {},
    "token_usage": {
        "prompt_tokens": 35,
        "completion_tokens": 70,
        "total_tokens": 105
    }
}
```

### 2. コンポーネントの呼び出し
- SDKは、Baiduのエコシステムから提供される40以上の高品質なコンポーネントを提供しています。リストは[コンポーネントリスト](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz#3%E3%80%81%E5%BC%80%E9%80%9A%E7%BB%84%E4%BB%B6%E6%9C%8D%E5%8A%A1)で確認できます。呼び出す前に[無料試用クォータ](https://console.bce.baidu.com/ai/#/ai/apaas/overview/resource/getFree)を申請してください。
- 例のコンポーネントは`RAG with Baidu Search Pro`で、Baidu Searchの検索エンジン技術とERNIEモデルのセマンティック理解能力を組み合わせて、ユーザーの検索意図をより正確に理解し、検索クエリに関連性の高い検索結果を提供します。

#### コード例
```python
import appbuilder
import os

# 環境変数にTOKENを設定します。以下のTOKENはアクセスとQPSが制限された試用TOKENです。正式な使用には個人のTOKENに置き換えてください。
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

rag_with_baidu_search_pro = appbuilder.RagWithBaiduSearchPro(model="ERNIE-Lite-AppBuilder-8K")

input = appbuilder.Message("9.11と9.8のどちらが大きいですか？")
result = rag_with_baidu_search_pro.run(
    message=input,
    instruction=appbuilder.Message("あなたは専門知識アシスタントです"))

# 実行結果を出力します。
print(result.model_dump_json(indent=4))
```

#### 回答表示
```shell
{
    "content": "9.11は9.8より小さいです。小数の大小を比較する際には、整数部分と小数部分の数値を逐次比較する必要があります。9.11と9.8の場合、整数部分はどちらも9なので、小数部分で比較する必要があります。小数点後の最初の桁は1と8であり、明らかに1は8より小さいため、9.11は9.8より小さいです。",
    "name": "msg",
    "mtype": "dict",
    "id": "eb31b7de-dd6a-485f-adb9-1f7921a6f4bf",
    "extra": {
        "search_baidu": [
            {
                "content": "大規模モデルの「知能」が疑問視される:9.11 vs 9...",
                "icon": "https://appbuilder.bj.bcebos.com/baidu-search-rag-pro/icon/souhu.ico",
                "url": "https://m.sohu.com/a/793754123_121924584/",
                "ref_id": "2",
                "site_name": "搜狐网",
                "title": "大規模モデルの「知能」が疑問視される:9.11 vs 9.8の比較がAIの理解能力を明らかにする..."
            },
            {
                "content": "究極|9.11は9.8より大きい？大規模モデルはなぜ...",
                "icon": "https://appbuilder.bj.bcebos.com/baidu-search-rag-pro/icon/tencent.svg.png",
                "url": "https://new.qq.com/rain/a/20240717A07JLV00",
                "ref_id": "4",
                "site_name": "腾讯网",
                "title": "究極|9.11は9.8より大きい？大規模モデルはなぜ小学校の数学問題で集団的に..."
            },
            ...
        ]
    },
    "token_usage": {
        "completion_tokens": 77,
        "prompt_tokens": 2008,
        "total_tokens": 2085
    }
}
```


### 3. AIネイティブアプリケーションの呼び出し
- 例のアプリケーションは：[ラップメンター](https://appbuilder.baidu.com/s/3qfjXy7k)です。このリンクをクリックしてウェブページで試してみてください。

#### コード例

```python
import appbuilder
import os

# 環境変数にTOKENを設定します。以下のTOKENはアクセスとQPSが制限された試用TOKENです。正式な使用には個人のTOKENに置き換えてください。
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-n5AYUIUJMarF7F7iFXVeK/1bf65eed7c8c7efef9b11388524fa1087f90ea58"

# AppBuilderのウェブページからアプリケーションIDを取得し、以下にラップメンターのアプリケーションIDを入力します。
app_id = "4678492a-5864-472e-810a-654538d3503c"

app_builder_client = appbuilder.AppBuilderClient(app_id)
conversation_id = app_builder_client.create_conversation()

answer = app_builder_client.run(conversation_id, "「上班狼狈却又追逐梦想」をテーマにラップを作成してください。押韻を保ち、200文字以内にしてください。")
print(answer.content.answer)
```

#### 回答表示
```shell
わかりました。「上班狼狈却又追逐梦想」をテーマに、簡単なラップを作成します。以下は簡単な例です。自分の感覚に合わせて調整してください。

イントロ:
朝九晚五、生活の重圧、
狼狈上班、しかし夢を追いかける、
毎日が新たな挑戦、
未来のために、私は前進する。

バース1:
スーツを着て、ネクタイを締めて、
人混みに入って、名声を追い求める、
狼狈しても、決して諦めない、
心の中に、夢があるから。

フック:
上班狼狈、しかし決して諦めない、
夢を追いかける、それが私の心の灯、
前方を照らし、私を導く、
どんなに困難でも、私は最後まで頑張る。

この小曲は「上班狼狈却又追逐梦想」をテーマに、押韻を通じて上班族が生活の苦しさにもかかわらず、夢を抱いて前進する精神を表現しています。気に入っていただけると幸いです！
```

**AIネイティブアプリケーションのコード例については、[Cookbooks](./cookbooks/README.md)をご覧ください。以下のクックブックを優先的にお勧めします：**
- 基本機能コンポーネント
    - [一般的なテキスト認識コンポーネント](/cookbooks/components/general_ocr.ipynb)
    - [基本コンポーネントのサービス指向デプロイメント](/cookbooks/components/agent_runtime.ipynb)
- プロセスオーケストレーション
    - [Assistant SDK](/cookbooks/pipeline/assistant_function_call.ipynb)
- エンドツーエンドアプリケーション
    - [エージェント](/cookbooks/agent_builder.ipynb)
    - [RAG](/cookbooks/end2end_application/rag/rag.ipynb)
    - [企業レベルのQ&Aシステム](/cookbooks/end2end_application/rag/qa_system_2_dialogue.ipynb)
- 高度な実践
    - [パブリッククラウドへのサービスデプロイメント](/cookbooks/advanced_application/cloud_deploy.ipynb)
    - [サービストレース](/cookbooks/appbuilder_trace/trace.ipynb)


## Baidu AI Cloud Qianfan AppBuilder SDKの機能全景
<div align="center">
<img src='image/structure-en.png' alt='wechat' width='800' >
</div>


## ユーザードキュメント

- [ホームページ](https://github.com/baidubce/app-builder/blob/master/docs/README.md)
    - クイックスタート: 
        - 最初のAIネイティブアプリケーションを開始する: 
            - [インストール](https://github.com/baidubce/app-builder/blob/master/docs/QuickStart/StartFirstAINativeApplication/install.md)
            - [クイックスタートガイド](https://github.com/baidubce/app-builder/blob/master/docs/QuickStart/StartFirstAINativeApplication/README.md)
        - 産業実践アプリケーション例: 
            - [SDK使用例](https://github.com/baidubce/app-builder/blob/master/docs/QuickStart/ExamplesOfIndustrialPracticeApplications/README.md)
        - [現在SDKがサポートしているプログラミング言語](https://github.com/baidubce/app-builder/blob/master/docs/QuickStart/CurrentlySupportedProgrammingLanguages/README.md)
    - 基本:
        - モデル:
            - [モデルリストの取得](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Model/get_model_list.md)
        - [コンポーネント](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Components/Components.md)
        - 監視:
            - [TRACE基本機能](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Trace/basic.md)
            - [TRACE拡張機能](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Trace/phoenix_method.md)
            - [Debug機能](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Trace/Debug.md)
        - デプロイ:
            - [インタラクティブなフロントエンドデプロイ](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Deployment/chainlit_deploy.md)
            - [パブリッククラウドデプロイ](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Deployment/cloud.md)
            - [API アクセス](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Deployment/flask_deploy.md)
            - [UserSession](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Deployment/usersession.md)
        - プラットフォーム:
            - アプリケーション:
                - [AppBuilderClientコンポーネント](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Platform/Application/appbuilder_client.md)
                - [AppBuilderで公開されたアプリケーションリストの取得](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Platform/Application/get_app_list.md)
            - ナレッジベース:
                - [ナレッジベースコンポーネント](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Platform/KnowledgeBase/knowledgebase.md)
            - カスタムコンポーネント:
                - [基本機能コンポーネント](https://github.com/baidubce/app-builder/blob/master/docs/BasisModule/Platform/CustomComponents/components.md)
    - アプリケーション:
        - エージェント:
            - [基本知識](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
            - [公式コンポーネントの使用](https://github.com/baidubce/app-builder/blob/master/docs/Application/Agent/UseOfficialComponents/use_official_components.md)
            - [ToolCall](https://github.com/baidubce/app-builder/blob/master/docs/Application/Agent/ToolCall/tool_call.md)
            - [ToolChoice](https://github.com/baidubce/app-builder/blob/master/docs/Application/Agent/ToolChoice/tool_choice.md)
            - [非同期およびストリーミングを使用してクライアント呼び出しを加速する](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
        - RAG:
            - [基本知識](https://github.com/baidubce/app-builder/blob/master/docs/Application/RAG/BasicKnowledge/rag.md)
            - [ナレッジベース管理](https://github.com/baidubce/app-builder/blob/master/docs/Application/RAG/DatasetManage/dataset_manage.md)
            - [Reference情報処理](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
        - ワークフロー:
            - [基本知識](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
            - [Workflowを使ってRAGアプリケーションをゼロから組み立てる](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
            - [Workflowを使ってAgentアプリケーションをゼロから組み立てる](https://github.com/baidubce/app-builder/blob/master/docs/Tools/DocPass/DocPass.md)
    - 開発者ガイド:
        - [コードの貢献方法](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/HowToContributeCode/README.md)
        - [にじかいせっか](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/AdvancedDevelopment/README.md)
        - [バージョンアップログ](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/ChangeLog/changelog.md)
        - [エラーメッセージ](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/ErrorMessage/error_message.md)
        - [環境パラメータ](https://github.com/baidubce/app-builder/blob/master/docs/DevelopGuide/EnvironmentalParameters/env.md)


## オープンソースコミュニティと活動
<div align="center">
<h3>AppBuilder-SDK WeChatグループQRコード</h3>
<img src='image/wechat_group.png' alt='wechat' width='200' >
</div>

- [Github Issue](https://github.com/baidubce/app-builder/issues):  インストール/使用の問題を提出し、バグを報告し、新機能を提案し、開発計画をコミュニケーションします。

- [Baidu AI Cloud Qianfan Community](https://cloud.baidu.com/qianfandev)



## ライセンス

AppBuilder SDKはApache 2.0オープンソースプロトコルに従います。


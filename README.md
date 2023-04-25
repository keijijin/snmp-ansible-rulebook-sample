# Ansible Rulebook - Hello Events

このプロジェクトは、Ansible Rulebook を使用して SNMP トラップイベントを監視し、特定の条件に一致するイベントが発生した場合に、指定されたアクションを実行するサンプルです。この例では、以下の設定が含まれています。

- SNMP トラップイベントの監視
- エージェントアドレスが "127.0.0.1" の場合にルールが適用される
- 条件に一致する場合、以下のアクションが実行されます:
  - `test_playbook.yml` プレイブックの実行
  - イベント情報の出力 (pretty-print)
  - デバッグメッセージの出力

## 前提条件

- Python 3.8 以上がインストールされていること
- Ansible Rulebook がインストールされていること

## インストール

以下のコマンドで Ansible Rulebook をインストールしてください。

```
pip install ansible-rulebook
```

## 起動

以下のコマンドでこのプロジェクトを起動します。

```
ansible-rulebook -S plugins -r test_rulebook.yml -i inventory/hosts
```

コマンドの説明:

- `-S plugins`: プラグインディレクトリを指定します。
- `-r test_rulebook.yml`: ルールブックの YAML ファイルを指定します。
- `-i inventory/hosts`: インベントリファイルを指定します。

## ルールブックの内容

このルールブックには、以下の設定が含まれています。

```yaml
---
- name: Hello Events
  hosts: localhost

  sources:
    - snmp_trap:
        host: 0.0.0.0
        port: 162
  
  rules:
    - name: Sample rule
      condition: event.snmp_trap.agentAddress == "127.0.0.1"
      actions:
        - run_playbook:
            name: test_playbook.yml
        - print_event:
            pretty: true
        - debug:
            msg: "SnmpTrap: {{ event.snmp_trap }}"
            # var: event.snmp_trap.agentAddress
...
```

この設定を適用すると、`localhost` で SNMP トラップイベントを監視し、エージェントアドレスが "127.0.0.1" の場合に、指定されたアクションが実行されます。

## アクションの説明

このルールブックでは、特定の条件に一致した場合に以下のアクションが実行されます。

1. **run_playbook**: このアクションは、指定されたプレイブックを実行します。この例では、`test_playbook.yml` が実行されます。プレイブックには、Ansible で実行するタスクが定義されています。

2. **print_event**: このアクションは、イベントの詳細を標準出力に表示します。`pretty: true` オプションを指定することで、整形された形式で出力されます。これにより、イベントの情報を確認しやすくなります。

3. **debug**: このアクションは、デバッグメッセージを表示します。この例では、`"SnmpTrap: {{ event.snmp_trap }}"` というメッセージが表示されます。`event.snmp_trap` の部分は、実際の SNMP トラップイベントの情報に置き換えられます。また、コメントアウトされた `var: event.snmp_trap.agentAddress` を有効にすると、エージェントアドレスの情報だけが表示されます。

## カスタマイズ

このルールブックは、条件やアクションを編集することで、さまざまなシナリオに対応できるようにカスタマイズできます。例えば、条件を変更して、異なるエージェントアドレスや OID に基づいてアクションを実行することができます。また、新しいアクションを追加して、条件に一致するイベントが発生したときに通知を送信するなど、さらに柔軟な対応が可能です。

## まとめ

Ansible Rulebook を使用すると、SNMP トラップイベントを監視し、特定の条件に一致した場合にアクションを実行することができます。このプロジェクトでは、エージェントアドレスが "127.0.0.1" の場合に、プレイブックの実行、イベント情報の出力、デバッグメッセージの表示といったアクションが実行されるサンプルが提供されています。このルールブックをカスタマイズすることで、さまざまなシナリオに対応する監視と自動対応が実現できます。
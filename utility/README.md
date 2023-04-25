# SNMP Trap Parser

このプログラムは、SNMPv1 トラップを解析し、デコードされたデータを Python のディクショナリ形式で提供します。これにより、SNMP トラップイベントを簡単に解析し、トラップ情報をプログラムで利用できるようになります。

## 機能

- SNMPv1 トラップのバイナリデータを解析
- トラップ情報をPythonディクショナリ形式で出力
- OIDのデコードをサポート

## 使用方法

1. まず、`decode_oid` 関数を使って、OIDバイナリデータをデコードします。
2. 次に、`parse_snmptrap_v1` 関数を使用して、SNMPv1 トラップのバイナリデータを解析し、Python ディクショナリ形式でトラップ情報を取得します。
3. 最後に、解析されたトラップ情報を使用して、プログラムで必要な操作を実行できます。

## 例

以下のコードは、プログラムを実行するための簡単なサンプルです。

```python
binary_data = b'0l\x02\x01\x00\x04\x06public\xa4_\x06\x0c+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#@\x04\x7f\x00\x00\x01\x02\x01\x00\x02\x02\x03\xe7C\x04\x06a\xcb\x8f0<0\x19\x06\x10+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#\x00\x87g\x01\x04\x05123450\x1f\x06\x10+\x06\x01\x04\x01\xbf\x08\xce\x0f\x00\x02#\x00\x87g\x02\x04\x0bHello World'

trap_v1_parameters = parse_snmptrap_v1(binary_data)
print(json.dumps(trap_v1_parameters, indent=2))
```

このサンプルでは、`binary_data` として指定された SNMPv1 トラップを解析し、その結果を JSON 形式で出力します。
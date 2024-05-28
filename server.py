import socket
import os
import server_func
import json

string_callable = {
    "floor": server_func.floor,
    "nroot": server_func.nroot,
    "reverse": server_func.reverse,
    "validAnagram": server_func.validAnagram,
    "sort": server_func.sort
}

result = {
    "results": "-1",
    "id": "-1"
}

# リクエスト処理関数
def handle_request(function_name, params):
    if function_name in string_callable:
        func = string_callable[function_name]
        if function_name == "sort":
            return func(params)  # Pass the whole list as a single parameter
        else:
            return func(*params)  # Unpack parameters for other functions
    else:
        raise ValueError(f"Function {function_name} not found")

# リクエスト処理関数2
def server_response(data_dict):
    result["id"] = data_dict["id"] 
    result["results"] = handle_request(data_dict["method"], data_dict["params"])
    return result

def main():
    # UNIXソケットをストリームモードで作成します
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # このサーバが接続を待つUNIXソケットのパスを設定します
    server_address = '/tmp/socket_file'

    # 以前の接続が残っていた場合に備えて、サーバアドレスをアンリンク（削除）します
    try:
        os.unlink(server_address)
    # サーバアドレスが存在しない場合、例外を無視します
    except FileNotFoundError:
        pass

    print('Starting up on {}'.format(server_address))

    # サーバアドレスにソケットをバインド（接続）します
    sock.bind(server_address)

    # ソケットが接続要求を待機するようにします
    sock.listen(1)

    # 無限ループでクライアントからの接続を待ち続けます
    while True:
        # クライアントからの接続を受け入れます
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            # ループが始まります。これは、サーバが新しいデータを待ち続けるためのものです。
            while True:
                # ここでサーバは接続からデータを読み込みます。
                # 16という数字は、一度に読み込むデータの最大バイト数です。
                data = connection.recv(256)

                # 受け取ったデータはバイナリ形式なので、それを文字列に変換します。
                # 'utf-8'は文字列のエンコーディング方式です。
                data_str =  data.decode('utf-8')

                # 受け取ったデータを表示します。
                print('Received ' + data_str)

                # もしデータがあれば（つまりクライアントから何かメッセージが送られてきたら）以下の処理をします。
                if data:
                    # 受け取ったメッセージを処理します。
                    data_dict = json.loads(data_str) 
                    server_response(data_dict)  # Updated to pass data_dict to server_action
                    json_result = json.dumps(result)
                    bytes_result = json_result.encode('utf-8')

                    #追加
                    connection.sendall(bytes_result)

                    # 処理したメッセージをクライアントに送り返します。
                    # ここでメッセージをバイナリ形式（エンコード）に戻してから送信します。

                # クライアントからデータが送られてこなければ、ループを終了します。
                else:
                    print('no data from', client_address)
                    break

        # 最終的に接続を閉じます
        finally:
            print("Closing current connection")
            connection.close()

main()

# Install
次のコマンドでアプリケーションに必要なモジュールをインストールする。

``` shell
yarn install
```

# フォーマッタ
次のコマンドでプロジェクト全体のソースコードを自動フォーマットします。

``` shell
"yarn run prettier --write .
```

また、VSCODEに拡張機能`emeraldwalk.runonsave`を入れると、ファイル保存時に自動フォーマットが行われます。
ただし、この拡張機能はコマンドを実行するため、悪意あるプロジェクトをVSCODEで編集するとバックドアを仕込まれる可能性があります。

拡張機能導入後、`sample.ts`などを作成し、次のコードをエディタで保存すると自動フォーマットされるはずです。

```
function test(){
    console.log("test");;;;;;;
        console.log("test");;;;;;;
}
```

# Debug
次のコマンドでデバッグアプリケーションを起動する。

```
yarn dev
```

# 開発時の注意

## scriptタグをtypescriptだと認識させる。
```typescript
<script lang="ts"></script>
```

# memo

```bash
# install dependencies
$ yarn install

# serve with hot reload at localhost:3000
$ yarn dev

# build for production and launch server
$ yarn build
$ yarn start

# generate static project
$ yarn generate
```
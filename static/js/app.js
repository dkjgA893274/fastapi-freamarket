// JavaScriptファイル - ページの動的な機能を制御するファイル

// アプリケーションの設定
const API_BASE_URL = 'http://localhost:8000'; // FastAPIサーバーのURL
let currentUser = null; // 現在ログインしているユーザー情報
let accessToken = null; // 認証トークン

// DOM要素の取得（ページが読み込まれた後に実行）
document.addEventListener('DOMContentLoaded', function() {
    // ページが完全に読み込まれた後に実行される処理

    // 各ボタンとフォームの要素を取得
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const loginFormElement = document.getElementById('loginFormElement');
    const signupFormElement = document.getElementById('signupFormElement');
    const addItemForm = document.getElementById('addItemForm');

    // イベントリスナー（ボタンクリック時の処理）を設定
    loginBtn.addEventListener('click', () => showLoginForm());
    signupBtn.addEventListener('click', () => showSignupForm());
    logoutBtn.addEventListener('click', () => logout());

    // フォーム送信時のイベントリスナーを設定
    loginFormElement.addEventListener('submit', handleLogin);
    signupFormElement.addEventListener('submit', handleSignup);
    addItemForm.addEventListener('submit', handleAddItem);

    // 初期状態の設定
    checkAuthStatus();
});

// ログインフォームを表示する関数
function showLoginForm() {
    // 新規登録フォームを非表示に
    document.getElementById('signupForm').style.display = 'none';
    // ログインフォームを表示
    document.getElementById('loginForm').style.display = 'block';
    // 認証セクションを表示
    document.getElementById('authSection').style.display = 'block';
    // 商品セクションを非表示に
    document.getElementById('itemSection').style.display = 'none';
}

// 新規登録フォームを表示する関数
function showSignupForm() {
    // ログインフォームを非表示に
    document.getElementById('loginForm').style.display = 'none';
    // 新規登録フォームを表示
    document.getElementById('signupForm').style.display = 'block';
    // 認証セクションを表示
    document.getElementById('authSection').style.display = 'block';
    // 商品セクションを非表示に
    document.getElementById('itemSection').style.display = 'none';
}

// ログイン処理を行う関数
async function handleLogin(event) {
    event.preventDefault(); // フォームのデフォルト送信を防ぐ

    // フォームからユーザー名とパスワードを取得
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        // ログインAPIを呼び出し
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        });

        if (response.ok) {
            // ログイン成功
            const data = await response.json();
            accessToken = data.access_token; // トークンを保存
            currentUser = { username: username }; // ユーザー情報を保存

            // ローカルストレージにトークンを保存（ページをリロードしても保持）
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));

            showMessage('ログインに成功しました！', 'success');
            showItemSection(); // 商品管理画面を表示
            loadItems(); // 商品一覧を読み込み
        } else {
            // ログイン失敗
            const errorData = await response.json();
            showMessage('ログインに失敗しました: ' + (errorData.detail || 'ユーザー名またはパスワードが間違っています'), 'error');
        }
    } catch (error) {
        // ネットワークエラーなどの例外処理
        console.error('ログインエラー:', error);
        showMessage('ログイン中にエラーが発生しました', 'error');
    }
}

// 新規登録処理を行う関数
async function handleSignup(event) {
    event.preventDefault(); // フォームのデフォルト送信を防ぐ

    // フォームからユーザー名とパスワードを取得
    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;

    try {
        // 新規登録APIを呼び出し
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        if (response.ok) {
            // 登録成功
            showMessage('ユーザー登録に成功しました！ログインしてください。', 'success');
            // ログインフォームに切り替え
            showLoginForm();
            // フォームをクリア
            document.getElementById('signupUsername').value = '';
            document.getElementById('signupPassword').value = '';
        } else {
            // 登録失敗
            const errorData = await response.json();
            showMessage('登録に失敗しました: ' + (errorData.detail || 'エラーが発生しました'), 'error');
        }
    } catch (error) {
        // ネットワークエラーなどの例外処理
        console.error('登録エラー:', error);
        showMessage('登録中にエラーが発生しました', 'error');
    }
}

// ログアウト処理を行う関数
function logout() {
    // ユーザー情報とトークンをクリア
    currentUser = null;
    accessToken = null;

    // ローカルストレージからも削除
    localStorage.removeItem('accessToken');
    localStorage.removeItem('currentUser');

    // 認証画面を表示
    showAuthSection();
    showMessage('ログアウトしました', 'info');
}

// 認証状態をチェックする関数
function checkAuthStatus() {
    // ローカルストレージからトークンとユーザー情報を取得
    const savedToken = localStorage.getItem('accessToken');
    const savedUser = localStorage.getItem('currentUser');

    if (savedToken && savedUser) {
        // 保存された情報がある場合はログイン状態にする
        accessToken = savedToken;
        currentUser = JSON.parse(savedUser);
        showItemSection(); // 商品管理画面を表示
        loadItems(); // 商品一覧を読み込み
    } else {
        // 保存された情報がない場合は認証画面を表示
        showAuthSection();
    }
}

// 認証セクションを表示する関数
function showAuthSection() {
    document.getElementById('authSection').style.display = 'block';
    document.getElementById('itemSection').style.display = 'none';
    document.getElementById('loginBtn').style.display = 'inline-block';
    document.getElementById('signupBtn').style.display = 'inline-block';
    document.getElementById('logoutBtn').style.display = 'none';
}

// 商品管理セクションを表示する関数
function showItemSection() {
    document.getElementById('authSection').style.display = 'none';
    document.getElementById('itemSection').style.display = 'block';
    document.getElementById('loginBtn').style.display = 'none';
    document.getElementById('signupBtn').style.display = 'none';
    document.getElementById('logoutBtn').style.display = 'inline-block';
}

// 商品追加処理を行う関数
async function handleAddItem(event) {
    event.preventDefault(); // フォームのデフォルト送信を防ぐ

    // フォームから商品情報を取得
    const name = document.getElementById('itemName').value;
    const description = document.getElementById('itemDescription').value;
    const price = parseInt(document.getElementById('itemPrice').value);

    try {
        // 商品追加APIを呼び出し
        const response = await fetch(`${API_BASE_URL}/items`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}` // 認証トークンを送信
            },
            body: JSON.stringify({
                name: name,
                description: description,
                price: price
            })
        });

        if (response.ok) {
            // 商品追加成功
            const newItem = await response.json();
            showMessage('商品を追加しました！', 'success');

            // フォームをクリア
            document.getElementById('itemName').value = '';
            document.getElementById('itemDescription').value = '';
            document.getElementById('itemPrice').value = '';

            // 商品一覧を再読み込み
            loadItems();
        } else {
            // 商品追加失敗
            const errorData = await response.json();
            showMessage('商品の追加に失敗しました: ' + (errorData.detail || 'エラーが発生しました'), 'error');
        }
    } catch (error) {
        // ネットワークエラーなどの例外処理
        console.error('商品追加エラー:', error);
        showMessage('商品追加中にエラーが発生しました', 'error');
    }
}

// 商品一覧を読み込む関数
async function loadItems() {
    try {
        // 商品一覧取得APIを呼び出し
        const response = await fetch(`${API_BASE_URL}/items`, {
            headers: {
                'Authorization': `Bearer ${accessToken}` // 認証トークンを送信
            }
        });

        if (response.ok) {
            // 商品一覧取得成功
            const items = await response.json();
            displayItems(items); // 商品一覧を表示
        } else {
            // 商品一覧取得失敗
            showMessage('商品一覧の取得に失敗しました', 'error');
        }
    } catch (error) {
        // ネットワークエラーなどの例外処理
        console.error('商品一覧取得エラー:', error);
        showMessage('商品一覧の取得中にエラーが発生しました', 'error');
    }
}

// 商品一覧を表示する関数
function displayItems(items) {
    const container = document.getElementById('itemsContainer');
    container.innerHTML = ''; // 既存の内容をクリア

    if (items.length === 0) {
        // 商品がない場合
        container.innerHTML = '<p style="text-align: center; color: #666; grid-column: 1 / -1;">商品がありません。新しい商品を追加してください。</p>';
        return;
    }

    // 各商品をカード形式で表示
    items.forEach(item => {
        const itemCard = createItemCard(item);
        container.appendChild(itemCard);
    });
}

// 商品カードを作成する関数
function createItemCard(item) {
    // 商品カードのHTML要素を作成
    const card = document.createElement('div');
    card.className = 'item-card';
    card.innerHTML = `
        <div class="item-name">${escapeHtml(item.name)}</div>
        <div class="item-description">${escapeHtml(item.description)}</div>
        <div class="item-price">¥${item.price.toLocaleString()}</div>
        <div class="item-actions">
            <button class="btn btn-danger" onclick="deleteItem(${item.id})">削除</button>
        </div>
    `;
    return card;
}

// 商品削除処理を行う関数
async function deleteItem(itemId) {
    // 削除確認
    if (!confirm('この商品を削除しますか？')) {
        return;
    }

    try {
        // 商品削除APIを呼び出し
        const response = await fetch(`${API_BASE_URL}/items/${itemId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}` // 認証トークンを送信
            }
        });

        if (response.ok) {
            // 商品削除成功
            showMessage('商品を削除しました！', 'success');
            loadItems(); // 商品一覧を再読み込み
        } else {
            // 商品削除失敗
            const errorData = await response.json();
            showMessage('商品の削除に失敗しました: ' + (errorData.detail || 'エラーが発生しました'), 'error');
        }
    } catch (error) {
        // ネットワークエラーなどの例外処理
        console.error('商品削除エラー:', error);
        showMessage('商品削除中にエラーが発生しました', 'error');
    }
}

// メッセージを表示する関数
function showMessage(message, type = 'info') {
    const messageArea = document.getElementById('messageArea');

    // メッセージ要素を作成
    const messageElement = document.createElement('div');
    messageElement.className = `message ${type}`;
    messageElement.textContent = message;

    // メッセージエリアに追加
    messageArea.appendChild(messageElement);

    // 3秒後に自動で削除
    setTimeout(() => {
        if (messageElement.parentNode) {
            messageElement.parentNode.removeChild(messageElement);
        }
    }, 3000);
}

// HTMLエスケープ関数（XSS攻撃を防ぐため）
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
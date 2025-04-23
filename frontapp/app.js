const apiUrl = "http://127.0.0.1:8000/memos/";

// Define functions
let editingMemoId = null;

function displayMessage(message) {
    alert(message);
}

function resetForm() {
    document.getElementById("formTitle").textContent = "メモの作成";
    document.getElementById("title").value = "";
    document.getElementById("description").value = "";
    // CSSに対してdisplay: noneを設定
    document.getElementById("updateButton").style.display = "none";
    document.querySelector(
        '#createMemoForm button[type="submit"]'
    ).style.display = "block";
    editingMemoId = null;
}

async function createMemo(memo) {
    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-type": "application/json" },
            body: JSON.stringify(memo),
        });
        const data = await response.json();
        if (response.ok) {
            displayMessage(data.message);
            resetForm();
            await fetchAndDisplayMemos();
        } else {
            // 422ステータスは自作したAPIからエラー時に返ってくるステータスコード。
            if (response.status === 422) {
                displayMessage("入力内容に誤りがあります。");
            } else {
                displayMessage(data.detail);
            }
        }
    } catch (err) {
        console.error("メモ作成中にエラーが発生しました: ", err);
    }
}

async function updateMemo(memo) {
    try {
        const response = await fetch(`${apiUrl}${editingMemoId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(memo),
        });
        const data = await response.json();
        if (response.ok) {
            displayMessage(data.message);
            resetForm();
            await fetchAndDisplayMemos();
        } else {
            if (response.status === 422) {
                displayMessage("入力内容に誤りがあります。");
            } else {
                displayMessage(data.detail);
            }
        }
    } catch (err) {
        console.error("メモ更新中にエラーが発生しました: ", err);
    }
}

async function deleteMemo(memoId) {
    try {
        const response = await fetch(`${apiUrl}${memoId}`, {
            method: "DELETE",
        });
        const data = await response.json();
        if (response.ok) {
            displayMessage(data.message);
            await fetchAndDisplayMemos();
        } else {
            displayMessage(data.detail);
        }
    } catch (err) {
        console.error("メモの削除中にエラーが発生しました: ", err);
    }
}

async function fetchAndDisplayMemos() {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const memos = await response.json();
        const memosTableBody = document.querySelector("#memos tbody");
        memosTableBody.innerHTML = "";
        memos.forEach((memo) => {
            const row = document.createElement("tr");
            row.innerHTML = `
            <td>${memo.title}</td>
            <td>${memo.description}</td>
            <td>
                <button class="edit" data-id="${memo.memo_id}">編集</button>
                <button class="delete" data-id="${memo.memo_id}">削除</button>
            </td>
            `;
            memosTableBody.appendChild(row);
        });
    } catch (err) {
        console.error("メモ一覧の取得中にエラーが発生しました: ", err);
    }
}

async function editMemo(memoId) {
    editingMemoId = memoId;
    const response = await fetch(`${apiUrl}${memoId}`);
    const memo = await response.json();
    if (!response.ok) {
        displayMessage(memo.detail);
        return;
    }
    document.getElementById("title").value = memo.title;
    document.getElementById("description").value = memo.description;
    document.getElementById("formTitle").textContent = "メモの編集";
    document.getElementById("updateButton").style.display = "block";
    document.querySelector(
        '#createMemoForm button[type="submit"]'
    ).style.display = "none";
}

// Set event lintner
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("createMemoForm");
    form.onsubmit = async (event) => {
        event.preventDefault();
        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
        const memo = { title, description };
        if (editingMemoId) {
            await updateMemo(memo);
        } else {
            await createMemo(memo);
        }
    };

    document.getElementById("updateButton").onclick = async () => {
        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;
        await updateMemo({ title, description });
    };

    document
        .querySelector("#memos tbody")
        .addEventListener("click", async (event) => {
            if (event.target.className === "edit") {
                const memoId = event.target.dataset.id;
                await editMemo(memoId);
            } else if (event.target.className === "delete") {
                const memoId = event.target.dataset.id;
                await deleteMemo(memoId);
            }
        });
});

document.addEventListener("DOMContentLoaded", fetchAndDisplayMemos);

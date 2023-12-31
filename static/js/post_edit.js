document.addEventListener('DOMContentLoaded', function() {
    const addImageButton = document.getElementById('add_image_button');
    const newImageInput = document.getElementById('new_image');
    const deleteImageCheckbox = document.getElementById('delete_image');
    const currentImage = document.querySelector('img'); // 現在の画像を取得
    const newImagePreview = document.getElementById('new_image_preview'); // 新しい画像のプレビューエリアを取得
    
    addImageButton.addEventListener('click', function() {
        newImageInput.click(); // 「新しい画像を選択」フィールドをクリック
    });
    
    // 新しい画像を選択した際の処理（プレビュー表示）
    newImageInput.addEventListener('change', function() {
        const file = newImageInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const previewImage = document.createElement('img');
                previewImage.src = event.target.result;
                previewImage.alt = 'New Image Preview';
                previewImage.width = 300;
                
                // プレビューを表示するための要素に追加
                newImagePreview.innerHTML = ''; // 以前のプレビューをクリア
                newImagePreview.appendChild(previewImage);
            };
            reader.readAsDataURL(file);
        }
    });

    // チェックボックスが変更された時の処理
    deleteImageCheckbox.addEventListener('change', function() {
        if (deleteImageCheckbox.checked) {
            currentImage.style.display = 'none'; // 画像を非表示にする例
            // 画像を削除するための追加の処理を行う（実際に画像を削除するためのコードを追加する必要があります）
        } else {
            currentImage.style.display = 'block'; // 画像を表示する例
            // 画像を削除するための追加の処理を元に戻す（実際のコードに合わせて修正）
        }
    });
});

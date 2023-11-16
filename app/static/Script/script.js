$(function () {
    async function sendRequest(url, method, data) {
        return new Promise((res, reject) => {
            $.ajax({
                url: url,
                method: method,
                data: data,
                processData: false,
                contentType: false,
                success: res,
                error: reject
            });
        });
    }

    let FileOrInput = 0;
    let files = undefined;
    let File = $("#inputFile");
    let Text = $("#inputText");
    Text.css("display", "none");
    File.css("display", "block");

    $("#formFile1").change(function (event) {
        // 首先移除所有的列表
        $("#file-list-container").empty();
        $("#pagination").css({
            "display": "none"
        });
        files = event.target.files;
        let file_count = files.length;
        console.log(file_count);
        if (file_count > 0)
            $("#slide_down_button").prop('disabled', false);
        if (file_count > 5) {
            $("#pagination").show();
        }

        let new_item = "<li class=\"list-group-item\">\n" +
            "                        <input class=\"form-check-input me-1\" type=\"checkbox\" value=\"\">\n" +
            "                        <label class=\"form-check-label\"  for=\"firstCheckbox\"></label>\n" +
            "                    </li>";
        for (let i = 0; i < file_count; i++)
            $("#file-list-container").append(new_item);

        // 遍历列表项，向其中添加元素
        $("#file-list-container label").each((index, element) => {
            console.log(element);
            let file_name = files[index].name;
            if (file_name.length > 20) {
                let splited_array = file_name.split('.');
                file_name = splited_array[0].substring(0, 5) + '...' + splited_array.pop();
            }
            element.innerHTML = file_name;
        });


    })

    $("#CommitBtn").click(function (event) {
        const length = files.length;
        let successCount = 0;
        let failList = [];
        let fileArray = Array.from(files);
        let formArray = Array();
        fileArray.forEach((element, index) => {
            let form = new FormData();
            form.append('file1', element);
            formArray.push(form);
        });
        console.log(fileArray);
        formArray.forEach((file) => {
            sendRequest('/upload_file', 'POST', file)
                .then(res => {
                    successCount++;
                }).catch(error => {
                failList.push(file.fileName);
                console.log(error);
            });
        });
        failList.forEach((value, index) => {
            console.log(value.name);
        });
    });

    $("#btnradio1").click(function (event) {
        // 点击了按钮一以后,表示用户要提交文件,那么文本框隐藏
        console.log("click radio1")
        FileOrInput = 0;
        console.log(FileOrInput);
    })
});
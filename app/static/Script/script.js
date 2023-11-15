$(function () {
    function sendRequest(url, method, data) {
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
        files = event.target.files;
        console.log(files);
        if (files.length > 0)
            $("#slide_down_button").prop('disabled', false);

    })


    $("#slide_down_button").onclick(event => {
        // 为展开按钮添加事件函数
    })


    $("#CommitBtn").click(function (event) {
        const length = files.length;
        let successCount = 0;
        let failList = [];

        files.forEach(file => {
            sendRequest('/upload_file', 'POST', file)
                .then(res => {
                    successCount++;
                }).catch(error => {
                failList.push(file.fileName);
            })
        })

        // alert("以下文件上传失败：",)
        // 提示是否有文件上传失败.
    })

    $("#btnradio1").click(function (event) {
        // 点击了按钮一以后,表示用户要提交文件,那么文本框隐藏
        console.log("click radio1")
        FileOrInput = 0;
        console.log(FileOrInput);
    })
});
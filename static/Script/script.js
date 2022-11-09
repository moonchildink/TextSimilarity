$(function () {
    let FileOrInput = 0   //判断用户是上传文件还是直接上传文本,1为默认状态,表示文本
    let file1 = undefined;
    let file2 = undefined;
    let File = $("#inputFile");
    let Text = $("#inputText");
    Text.css("display", "none");
    File.css("display", "block");
    $("#formFile1").change(function (event) {
        file1 = event.target.files[0];
        if (file1) {
            console.log(file1);
        }
    })
    $("#formFile2").change((event) => {
        file2 = event.target.files[0];
        if (file2) {
            console.log(file2);
        }
    })

    function uploadText(event) {

        let text = $("#floatingTextarea1").val();
        let text2 = $("#floatingTextarea2").val();
        console.log(text);
        console.log(text2);
        event.preventDefault();
        let Form = new FormData();
        Form.append("text1", text);
        Form.append("text2", text2);
        $.ajax({
            url: "/text/",
            type: "POST",
            data: Form,
            processData: false,
            contentType: false,
            success: (result) => {
                alert("文本的相似度为:  " + result*100 + "%");
            }
        })

    }

    function uploadFile(event) {
        let Form = new FormData();
        Form.append("file1", file1);
        Form.append("file2", file2);
        $.ajax({
            url: "/text/file/",
            method: "POST",
            data: Form,
            processData: false,
            contentType: false,
            success: (res) => {
                console.log(res);
                alert('文件的相似度为:  ' + res*100 + '%');
            },
            error: (err) => {
                console.log(err);
                console.log(err.status);
            }

        })
    }

    $("#CommitBtn").click(function (event) {
        if (FileOrInput)
            uploadText(event)
        else {
            console.log(file1);  //此处可以获取到file
            console.log(file2);
            uploadFile(event);
        }
    })

    $("#btnradio1").click(function (event) {
        // 点击了按钮一以后,表示用户要提交文件,那么文本框隐藏
        console.log("click radio1")
        Text.css("display", "none");
        File.css("display", "block");
        FileOrInput = 0;
        console.log(FileOrInput);
    })
    $("#btnradio2").click(function (event) {
        console.log("click radio 2")
        File.css("display", "none");
        Text.css("display", 'block');
        FileOrInput = 1;
    })
});
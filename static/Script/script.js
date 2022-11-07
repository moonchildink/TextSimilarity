$(function(){
    let FileOrInput = 1   //判断用户是上传文件还是直接上传文本,1为默认状态,表示文本
    $("#uploadFileButton").click((event)=>{
        // 判断用户是否成功上传
        $("#uploadFileInput").click()
        FileOrInput = 0

    })
    function uploadText(event){
        let text = $("#input").val();
        console.log(text);
        event.preventDefault();
        $.ajax({
            url:"/text?text="+text,
            methods:"POST",
            success:(result)=>{  // 成功的话执行回调
                // 解析服务器发来的数据
                console.log(result);
                // 还需要做一个调跳转的页面
            }
        })
    }
    function uploadFile(event){
        $.ajax({
            url:"/text/file",
            method:"POST",
            data:fd,
            processData:false,
            contentType:false,
            success:(res)=>{
                alert("文件上传成功!");
                console.log(res);
            }

        })
    }
    $("#CommitBtn").click(function(event){
        if(FileOrInput)
            uploadText(event)
        else {
            let files = $("#uploadFileInput").prop('files');

            let data = new FormData();
            data.append('uploadFileInput',files[0])

            uploadFile(event)
        }
    })
});
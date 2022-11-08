$(function(){
    let FileOrInput = 1   //判断用户是上传文件还是直接上传文本,1为默认状态,表示文本
    let file = undefined;
    $("#formFile").change(function(event){
        file = event.target.files[0];
        if(file){
            console.log(file);
            FileOrInput = 0;
        }


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
        let Form = new FormData();
        Form.append("file",file);
        $.ajax({
            url:"/text/file",
            method:"POST",
            data:Form,
            async:false,
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
            console.log(file);  //此处可以获取到file
            uploadFile(event);
        }
    })
});
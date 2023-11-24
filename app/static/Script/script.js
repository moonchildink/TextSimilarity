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

    async function getRequest(url) {
        let currentTime = new Date().getTime();
        console.log(currentTime);
        return new Promise((res, reject) => {
            $.ajax({
                url: url,
                method: 'GET',
                processData: false,
                contentType: false,
                success: res,
                error: reject
            })
        })
    }

    let FileOrInput = 0;
    let files = undefined;
    let File = $("#inputFile");
    let Text = $("#inputText");
    // let nextPage =
    Text.css("display", "none");
    File.css("display", "block");
    let pagination1 = $("#pagination1");
    let myFileList = $("#myFileList");


    function init() {
        // myFileList.css({'display': 'none'});
        $("#file-list-container").empty();
        pagination1.hide();
    }


    function hide_all() {
        $("#uploadPage").hide();
        $("#myFilePage").hide();
        $("#showContentPage").show();
        $("#LeftSection").hide();
        $("#RightSection").hide();
        $("#titleLine").hide();
    }


    function addSpinner() {
        let spinner = "<div class=\"spinner-border\" id = \"spinner\" role=\"status\">\n" +
            "                <span class=\"visually-hidden spinner\">Loading...</span>\n" +
            "            </div>";
        $("#showContentPage").append(spinner);
    }


    $("#checkSimilarityButton").click((event) => {
        // 从服务器获取信息
        hide_all();
        addSpinner();
        getRequest('/most_similar')
            .then((res) => {
                $("#showContentPage #spinner").hide();
                let file1 = res.files[0];
                let file2 = res.files[1];
                let similar = res.value;
                let titleLine = $("#titleLine");
                titleLine.show();
                titleLine.text(file1 + "与" + file2 + "最为相似：" + similar.toString());
                return [file1, file2];
            }).then((res) => {
            getRequest('/get_docx/' + res[0]).then(response => {
                let left_section = $("#LeftSection");
                left_section.show();
                left_section.append(response);
            });
            return res[1];
        }).then((value) => {  // 其实此处pycharm给出的value的类型是不对的。value等于上边的res[1];
            getRequest('/get_docx/' + value).then(response2 => {
                let right_section = $("#RightSection");
                right_section.show();
                right_section.append(response2);
            });
        }).catch((reject) => {
            console.log(reject);
        })
    })

    $("#uploadFilePageNav").click((event) => {
        $("#uploadPage").show();
        $("#myFileList").hide();
        $("#pagination2").hide();
    });

    $("#myFilePageNav").click((event) => {
        $("#myFilePage").show();
        myFileList.show();
        myFileList.empty();
        $("#uploadPage").hide();

        // 向服务器请求我的全部文件
        getRequest('/my_file')
            .then((res) => {
                console.log(res);

                let list_item = "<div class=\"aaaa\">\n" +
                    "    <li class=\"list-group-item d-flex justify-content-between align-items-start\">\n" +
                    "        <div class=\"ms-2 me-auto\">\n" +
                    "            <div class=\"fw-bold\">\n" +
                    "                <p class=\"ppp\">tezt</p>\n" +
                    "            </div>\n" +
                    "            <p class='aaa'></p>\n" +
                    "        </div>\n" +
                    "    </li>    \n" +
                    "</div>";
                let my_file_count = res.file_count;
                let files = res.filenames;
                let authors = res.authors;
                // 添加列表项
                for (let i = 0; i < my_file_count; i++)
                    $("#myFileList").append(list_item);
                $(".ppp").each((index, element) => {
                    element.innerHTML = files[index];
                });
                $(".aaa").each((index, element) => {
                    element.innerHTML = authors[index];
                });


                let itemsPerPage = 10;
                let totalPages = Math.ceil(my_file_count / itemsPerPage);
                let currentPage = 1;


                function showPage(page) {
                    console.log("showPage");
                    $("#myFileList .aaaa").hide();
                    let startIndex = (page - 1) * itemsPerPage;
                    let endIndex = startIndex + itemsPerPage;
                    $("#myFileList .aaaa").slice(startIndex, endIndex).show();
                }


                function generatePagination() {
                    let previous = "<li class=\"page-item\" id='previous-page'>\n" +
                        "    <a class=\"page-link\" aria-label=\"Previous\">\n" +
                        "        <span aria-hidden=\"true\"> << </span>\n" +
                        "    </a>\n" +
                        "</li>";

                    let next = "<li class=\"page-item\" id='next-page'>\n" +
                        "    <a class=\"page-link\" aria-label=\"Previous\">\n" +
                        "        <span aria-hidden=\"true\"> >> </span>\n" +
                        "    </a>\n" +
                        "</li>";
                    let page_item = "<li class=\"page-item\"><a class=\"page-link\"> </a></li>";
                    $(".pagination").empty();
                    $(".pagination").append(previous);
                    for (let i = 1; i <= totalPages; i++) {
                        let li = $(page_item);
                        let aTag = li.find('a.page-link');
                        aTag.text(i);
                        if (i === currentPage)
                            li.addClass('active');
                        $(".pagination").append(li);
                    }
                    $(".pagination").append(next);
                }

                showPage(currentPage);
                generatePagination();
                $("#pagination2").on('click', 'li', function () {
                    console.log($(this)[0].id);
                    console.log($(this));
                    if ($(this)[0].id === 'previous-page' && currentPage > 1) {
                        showPage(currentPage - 1);
                    } else if ($(this)[0].id === 'next-page' && currentPage < totalPages) {
                        showPage(currentPage + 1);
                    } else {
                        currentPage = parseInt($(this).text());
                        console.log($(this)[0].innerText);
                        showPage(currentPage);
                    }
                    generatePagination();
                });
            }).catch((error) => {
            console.log(error);
        });
    });

    $("#formFile1").change(function (event) {
        // 首先移除所有的列表
        init();
        files = event.target.files;
        let file_count = files.length;
        let new_item = "<li class=\"list-group-item\">\n" +
            "                        <input class=\"form-check-input me-1\" type=\"checkbox\" value=\"\">\n" +
            "                        <label class=\"form-check-label\"  for=\"firstCheckbox\"></label>\n" +
            "                    </li>";
        for (let i = 0; i < file_count; i++)
            $("#file-list-container").append(new_item);

        $("#file-list-container label").each((index, element) => {
            console.log(element);
            let file_name = files[index].name;
            if (file_name.length > 20) {
                let splited_array = file_name.split('.');
                file_name = splited_array[0].substring(0, 5) + '...' + splited_array.pop();
            }
            element.innerHTML = file_name;
        });


        if (file_count > 0 && file_count <= 5) {
            $("#slide_down_button").prop('disabled', false);
            // previous_page.show();
            // next_page.show();
        } else {
            // previous_page.attr('disabled', false);
            // next_page.attr('disabled', false);
            // 需要进行分页
            // const pageCount = Math.floor(file_count / 5) + 1;
            // let currentPage = 1;
        }


    });

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
    });


});
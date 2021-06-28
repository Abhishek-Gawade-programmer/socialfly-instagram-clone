$j(window).on("load", function () {
    var csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    var get_message = document.getElementById("main_message");
    var question_frame_element = document.getElementById("question_frame");

    $j(get_message).hide();

    var next_question = document.getElementById("next_question");
    var previous_question = document.getElementById("previous_question");

    var all_question = document.getElementById("show_all_question");
    var all_question_frame = document.getElementById("all_question_frame");
    var bookmark_question = document.getElementById("bookmark_question");

    var report_question = document.getElementById("report_question");
    var submit_exam = document.getElementById("submit_exam");

    window.navigation_question = navigation_question;

    window.question_number = 1;

    function navigation_question(question_number) {
        window.question_number = question_number;
        $j.ajax({
            type: "POST",

            url: "/navigation-question/",

            data: {
                csrfmiddlewaretoken: csrftoken,

                page_number: question_number,
            },

            success: function (response) {
                $j(get_message).hide();

                if (response.next === "false") {
                    $j(next_question).addClass("disabled");
                } else {
                    if (window.question_number === 1) {
                        $j(previous_question).addClass("disabled");
                    } else {
                        $j(previous_question).removeClass("disabled");
                    }

                    $j(next_question).removeClass("disabled");

                    question_frame_element.innerHTML = ` <div class="card">
                                            <div class="card-header">
                                            <input type="hidden" name="csrfmiddlewaretoken" value="${response.csrf_token}">
                                                  
                                              <span class="btn btn-danger ">
                                              Q${question_number} </span> 
                                              <span style="margin-left: 20px;" id='question_title' data='${response.id}'>
                                              ${response.question_title}</span> 
                                            </div>

                                            <div class="card-body">
                                                  <ul class="list-group" style="display: inline;">
                                                        <input type="radio" id="${response.id}1" name="${response.id}" ${response.option_1.student_option}>
                                                        <label for="${response.id}1"><li  class="list-group-item bg-gradient-primary">${response.option_1.text}</li></label><br>
                                                        <input type="radio" id="${response.id}2" name="${response.id}" ${response.option_2.student_option}>
                                                        <label for="${response.id}2"><li  class="list-group-item bg-warning">${response.option_2.text}</li></label><br>
                                                        <input type="radio" id="${response.id}3" name="${response.id}" ${response.option_3.student_option}>
                                                        <label for="${response.id}3"><li  class="list-group-item bg-info">${response.option_3.text}</li></label><br>
                                                        <input type="radio" id="${response.id}4" name="${response.id}" ${response.option_4.student_option}>
                                                        <label for="${response.id}4"><li  class="list-group-item bg-light">${response.option_4.text}</li></label><br>
                                                  </ul>
                                            </div>
                                      </div>
                            `;

                    var get_question =
                        document.getElementById("question_title");

                    var current_question_id = get_question.getAttribute("data");

                    var option_1 = document.getElementById(
                        current_question_id + "1"
                    );
                    var option_2 = document.getElementById(
                        current_question_id + "2"
                    );
                    var option_3 = document.getElementById(
                        current_question_id + "3"
                    );
                    var option_4 = document.getElementById(
                        current_question_id + "4"
                    );

                    var all_options = [option_1, option_2, option_3, option_4];

                    all_options.forEach((item) =>
                        item.addEventListener("change", (event) => {
                            var option_number = item.id.slice(-1);

                            $j.ajax({
                                type: "POST",

                                url: "/save-question/",

                                data: {
                                    // 'csrfmiddlewaretoken':csrftoken,
                                    csrfmiddlewaretoken: csrftoken,

                                    pk: current_question_id,
                                    option: option_number,
                                },

                                success: function (response) {
                    get_message.innerHTML = `<strong>Question No :
                                                                                            <span id='question_number'>${question_number}</span></strong> 
                                                                                                Save with Option :<span id='answer_number'>${option_number}
                                                                                            </span>`;

                                    $j(get_message).show();
                                },
                            });
                        })
                    );
                }
            },
        });
    }

    navigation_question(window.question_number);

    next_question.addEventListener("click", (event) => {
        console.log("next");
        navigation_question(window.question_number + 1);
    });

    previous_question.addEventListener("click", (event) => {
        console.log(previous_question);

        console.log("previous");
        navigation_question(window.question_number - 1);
    });

    bookmark_question.addEventListener("click", (event) => {
        $j.ajax({
            type: "GET",
            url: "/toogle-bookmark/" + window.question_number + "/",

            success: function (response) {
                if (response.done) {
                    get_message.innerHTML = `<strong>Question No :
                                <span id='question_number'>${window.question_number}</span></strong> 
                                <span class="badge badge-danger badge-pill" style="font-size:120%">BookMarked</span>
                                `;
                } else {
                    get_message.innerHTML = `<strong>Question No :
                                    <span id='question_number'>${window.question_number}</span></strong> 
                                    <span class="badge badge-success badge-pill" style="font-size:120%">Removed From Bookmark</span>
                                        `;
                }

                $j(get_message).show();
            },
        });
    });

    all_question.addEventListener("click", (event) => {
        all_question_deatils();

        function all_question_deatils() {
            $j.ajax({
                type: "GET",

                url: "/get-all-question-details/",

                success: function (response) {
                    all_question = response.all_question_json;
                    let all_question_text_button = "";
                    for (i in all_question) {
                        if (all_question[i].student_option) {
                            if (all_question[i].bookmark) {
                                all_question_text_button =
                                    all_question_text_button +
                                    `<div data-dismiss="modal" onclick="function hi(){navigation_question(${
                                        parseInt(i) + 1
                                    })};hi()" class="col mt-3"> <a class="btn btn-sm btn-primary btn-block"  data="${i}" tabindex="-1" id='previous_question'><b>Q` +
                                    (parseInt(i) + 1) +
                                    '<span style="color:red">(' +
                                    all_question[i].student_option +
                                    ")</span>" +
                                    ` </b></a></div>`;
                            } else {
                                all_question_text_button =
                                    all_question_text_button +
                                    `<div data-dismiss="modal" onclick="function hi(){navigation_question(${
                                        parseInt(i) + 1
                                    })};hi()" class="col mt-3" ><a class="btn btn-sm btn-warning btn-block"  data="${i}" tabindex="-1" id='previous_question'><b>Q` +
                                    (parseInt(i) + 1) +
                                    '<span style="color:red">(' +
                                    all_question[i].student_option +
                                    ")</span>" +
                                    ` </b></a></div>`;
                            }
                        } else {
                            if (all_question[i].bookmark) {
                                all_question_text_button =
                                    all_question_text_button +
                                    `<div data-dismiss="modal" onclick="function hi(){navigation_question(${
                                        parseInt(i) + 1
                                    })};hi()" class="col mt-3" ><a class="btn btn-sm btn-primary btn-block"  data="${i}" tabindex="-1" id='previous_question'><b>Q` +
                                    (parseInt(i) + 1) +
                                    ` </b></a></div>`;
                            } else {
                                all_question_text_button =
                                    all_question_text_button +
                                    `<div data-dismiss="modal" onclick="function hi(){navigation_question(${
                                        parseInt(i) + 1
                                    })};hi()" class="col mt-3" ><a class="btn btn-sm btn-danger btn-block"  data="${i}" tabindex="-1" id='previous_question'><b>Q` +
                                    (parseInt(i) + 1) +
                                    ` </b></a></div>`;
                            }
                        }
                    }
                    all_question_frame.innerHTML = all_question_text_button;
                },
            });
        }
    });

    report_question.addEventListener("click", (event) => {
        report_question_fu();

        function report_question_fu() {
            var description_box = document.getElementById("description_box");
            $j.ajax({
                type: "GET",

                url:
                    "/report-question/" +
                    window.question_number +
                    "/'" +
                    description_box.value +
                    " '/",

                success: function (response) {
                    get_message.innerHTML = `<strong>Question No :
                                <span id='question_number'>${window.question_number}</span></strong> 
                                <span class="badge badge-danger badge-pill" style="font-size:120%">Reported</span>
                                `;

                    $j(get_message).show();
                },
            });
        }
    });

    submit_exam.addEventListener("click", (event) => {
        console.log("submit cl8ick");

        submit_exam_fuction();

        function submit_exam_fuction() {
            $j.ajax({
                type: "GET",

                url: "/submit-exam",

                success: function (response) {
                    window.location.replace(
                        "http://localhost:8000/submit-exam/"
                    );
                },
            });
        }
    });













});

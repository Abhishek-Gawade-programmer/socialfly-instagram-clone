$j(window).on("load", function() {
    let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    let follow_unfollow_buttons = document.querySelectorAll(".follow_unfollow_button");



    follow_unfollow_buttons.forEach((button) =>
        button.addEventListener("click", (event) => {
            socialflyuser = button.getAttribute('user_id');
             
            $j.ajax({
                type: "POST",

                url: window.location.origin + "/users/wants-follow-unfollow/",

                data: {
                    csrfmiddlewaretoken: csrftoken,
                    socialflyuser: socialflyuser
                },

                success: function(response) {

                    if ( response.action ==='Unfollow'){

                    	$j(button).addClass('unfollow_button')

                    }
                    else{
                    	$j(button).removeClass('unfollow_button')
                    }
                    button.textContent=response.action
                },


            });

        }));



});
$j(window).on("load", function() {
    // let follow_unfollow_button = document.getElementById("follow_unfollow_button");
    let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    let follow_unfollow_buttons = document.querySelectorAll(".follow_unfollow_button");

    let private_checkbox=document.getElementById('customSwitch1');
    let profile_update_alert_box=document.getElementById('profile_update_alert_box');
    let profile_update_massage=document.getElementById('profile_update_massage');


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

          private_checkbox.addEventListener("change", (event) => {
            $j(profile_update_alert_box).hide()
             
            $j.ajax({
                type: "POST",

                url: window.location.origin + "/users/change-private-status/",

                data: {
                    csrfmiddlewaretoken: csrftoken,
                },

                success: function(response) {
                    if (response) {
                        profile_update_massage.textContent='Your profile Updated successfully !!'
                        $j(profile_update_alert_box).show()
                    }


                    


                },


            });

        })












});
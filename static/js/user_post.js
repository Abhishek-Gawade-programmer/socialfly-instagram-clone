removetheimage=document.getElementById('removetheimage');
uploadtheimage=document.getElementById('uploadtheimage');
let csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

Dropzone.autoDiscover=false;

const md= new Dropzone('#my-dropzone',{

    url:window.location.origin + "/posts/post-image-upload/",
    parallelUploads: 5,
    maxFiles:5,
    clickable: true,
    maxFilesize:3,
    acceptedFiles:'.jpg,.png,.jpeg,.gif',
    autoProcessQueue: false,
    uploadMultiple:true,
    success : function(file, response){
        removetheimage.setAttribute('post_pk',response.post_pk)
        uploadtheimage.innerHTML='Add Caption'
        removetheimage.innerHTML='<i class="fas fa-ban"></i> Delete the post'
    },
});
$j("#uploadtheimage").click(function (e) {
    console.log('button is xclixkerf')
e.preventDefault();
md.processQueue();
});

 $j("#removetheimage").click(function (e) {
    post_pk=removetheimage.getAttribute('post_pk')
    e.preventDefault();
    md.removeAllFiles();
    if (post_pk) {
          $j.ajax({
            type: "POST",

            url: window.location.origin + "/posts/delete-post/",

            data: {
                csrfmiddlewaretoken: csrftoken,
                post_pk: post_pk
            },

            success: function(response) {
                console.log('repaposmdoiamsoci',response)
                            },


        });
    }
   
    });



var spiner_box=document.getElementById('spiner_box');
var page = 1;
var empty_page = false;
var block_request = false;
$j(window).scroll(function() {
var margin = $j(document).height() - $j(window).height() - 200;
if($j(window).scrollTop() > margin && empty_page == false &&
block_request == false) {
    spiner_box.style.removeProperty("display");
 block_request = true;
  page += 1;
  $j.get('?page=' + page, function(data) {
    if(data == '') {
      empty_page = true;
    }
    else {
      block_request = false;
      $j('#feed').append(data);
      spiner_box.style.display ="none"
    }
  });
}
});
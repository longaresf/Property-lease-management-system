$(document).ready(function(){
    $(".inm_cook").on('click', function(){
      var $item = $(this).prev().text();
      document.cookie = 'inm_id=' + $item + '; path=/; SameSite=Lax';
    });
    $(".inm_cook_2").on('click', function(){
      var $item = $(this).prev().prev().text();
      document.cookie = 'inm_id=' + $item + '; path=/; SameSite=Lax';
    });
    $(".inm_cook_3").on('click', function(){
      var $item = $(this).prev().prev().prev().text();
      document.cookie = 'inm_id=' + $item + '; path=/; SameSite=Lax';
    });
    $(".img_cook").click(function(){
      var $item = $(this).prev().text();
      document.cookie = 'img_cook=' + $item + '; path=/; SameSite=Lax';
    });
  });

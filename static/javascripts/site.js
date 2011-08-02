function getCookie(name) {
  var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r ? r[1] : undefined;
}

jQuery.ajaxSetup({
  data: {'_xsrf': getCookie('_xsrf')}
});

// Bookmark actions
$('ul#bookmarks').delegate('a[data-action]', 'click', function(event){
  event.preventDefault();
  var $bookmark = $(this).closest('.bookmark'),
      bookmark_id = $bookmark.attr('id').split('_')[1],
      action = $(this).data('action');

  $.post('/update', {id: bookmark_id, action: action}, function(data) {
    $bookmark.replaceWith(data);
  });
});

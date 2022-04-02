function send_message(socketname,data){
    socketname.send(JSON.stringify(data))
  }

let allow=1
// let prevrooms=[]
// function click_counter(room){
//   if(prevrooms.includes(room)==1){
//     response=0
//   }
//   else{
//     prevrooms.push(room)
//     response=1
//   }
//   return response
// }

$chat = $(".chat");
$profile = $(".user-profile");

/* ===================================
    Screen resize handler
====================================== */
const smallDevice = window.matchMedia("(max-width: 767px)");
const largeScreen = window.matchMedia("(max-width: 1199px)");
smallDevice.addEventListener("change", handleDeviceChange);
largeScreen.addEventListener("change", handleLargeScreenChange);

handleDeviceChange(smallDevice);
handleLargeScreenChange(largeScreen);

function handleDeviceChange(e) {
  if (e.matches) chatMobile();
  else chatDesktop();
}

function handleLargeScreenChange(e) {
  if (e.matches) profileToogleOnLarge();
  else profileExtraLarge();
}

function chatMobile() {
  $chat.addClass("chat--mobile");
}

function chatDesktop() {
  $chat.removeClass("chat--mobile");
}

function profileToogleOnLarge() {
  $profile.addClass("user-profile--large");
}

function profileExtraLarge() {
  $profile.removeClass("user-profile--large");
}

/* ===================================
    Events
====================================== */

$(".messaging-member").click(function () {
  $chat.fadeIn();
  $chat.addClass("chat--show");
});

$(".chat__previous").click(function () {
  $chat.removeClass("chat--show");
});

$(".chat__details").click(function () {
  $profile.fadeIn();
  $profile.addClass("user-profile--show");
});

$(".user-profile__close").click(function () {
  $profile.removeClass("user-profile--show");
});

$(".messages-page__dark-mode-toogler").click(function () {
  $("body").toggleClass("dark-mode");
});


// custom js...................................
// add_member js

// members list open close
$('.add_members').click(function(e){
  if ($('.add_members').html()!=''){
    if($('.add_member_box').hasClass('add_member_show')==true){
      $('.add_member_box').removeClass('add_member_show')
      $('.add_member_box').addClass('add_member_close')
    }
    else{
      $('.add_member_box').removeClass('add_member_close')
      $('.add_member_box').addClass('add_member_show')
    }
  }

})


$('.add_memberclose_icon').click(function(e){
  $('.add_member_box').removeClass('add_member_show')
  $('.add_member_box').addClass('add_member_close')
})





// create_room js
$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New message to ' + recipient)
  modal.find('.modal-body input').val(recipient)
})


$('#create_room').submit(function(e){
  e.preventDefault()
  $.ajax({
    type:'POST',
    url:'newroom',
    data:$('#create_room').serialize(),
    success:function(res){
      // let res=JSON.parse(res)
      $('#msg').html(res.msg)
      location.reload();
    },
    error:function(){
      alert('no connection')
    }

  })
})





// users search
$("body").on("keydown", "#search_members", function(e){
  let keyword=$(this).val()
  let room=$(this).attr('target')
  let currentuser=$(this).attr('currentuser')
  if(keyword==''){
    $('.members_search_result').html('')
  }
  else{
      $.ajax({
    type:'GET',
    data:{
      'keyword':keyword,
      'room':room,
      'currentuser':currentuser
    },
    url:'searchmember',
    success:function(res){
      result=res.data
      let members=result[0]
      let users=result[1]
      if(users.length==0){
        $('.members_search_result').html('user not found')
      }
      else{
        $('.members_search_result').html('')
        for(i=users.length-1;i>=0;i--){
          if(members.length==0){
            $('.members_search_result').append('<li class="searchli"><img class="searchimg" src="https://randomuser.me/api/portraits/thumb/men/74.jpg" alt="Bessie Cooper" loading="lazy"><span>'+users[i]+'</span>|<button id="add_'+users[i]+'"    mission="add" class="addremove_member_button  btn btn-primary btn-sm" target="'+room+'" user="'+users[i]+'" type="button">add</button></li>')

          }
          for(j=members.length-1;j>=0;j--){
            if(users[i]==members[j]){
              $('.members_search_result').append('<li class="searchli"><img class="searchimg" src="https://randomuser.me/api/portraits/thumb/men/74.jpg" alt="Bessie Cooper" loading="lazy"><span>'+users[i]+'</span>|<button id="remove_'+users[i]+'" mission="remove" class="addremove_member_button btn btn-danger btn-sm" target="'+room+'" user="'+users[i]+'" type="button">remove</button></li>')
              
            }
            else if(users[i]!=members[j]){
              $('.members_search_result').append('<li class="searchli"><img class="searchimg" src="https://randomuser.me/api/portraits/thumb/men/74.jpg" alt="Bessie Cooper" loading="lazy"><span>'+users[i]+'</span>|<button id="add_'+users[i]+'"    mission="add" class="addremove_member_button  btn btn-primary btn-sm" target="'+room+'" user="'+users[i]+'" type="button">add</button></li>')

            }
          }
        }
      }
    },
    error:function(){
      console.log('error in connection')
    }
  })
  }
})
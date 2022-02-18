$(document).ready(function(){
$('#login_form').submit(function(e){
    e.preventDefault()
    $.ajax({
        type:'POST',
        url:'login',
        data:$('#login_form').serialize(),
        success:function(res){
            if(res.loginresponse=='true'){
                window.location.href = '/chat';
            }
            else{
                $('#error').html('نام کاربری و یا رمز شما اشتباه میباشد')
            }
        },
        error:function(){
            alert('خطا در برقراری ارتباط')
        }
    })
})




$('.link_room').click(function(e){
  e.preventDefault()
  let target=$(this).attr('target')
  $.ajax({
    type:'GET',
    url:'chat/'+target,
    data:{'room_name':target},
    success:function(res){
      $('.chat-with').html(res.room_name)
      for (i=res.members.length;i>=0;i--){
        $('.members').html('')
        $('.members').append(res.members[i]+',')
      }

      const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + res.room_name
        + '/'
    );

    chatSocket.onopen=function(e){
      
    }


    chatSocket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      $('.chat-message-list').append('<li class="clearfix"><div class="message-data align-right"><span class="message-data-time" >message_time</span> &nbsp; &nbsp;<span class="message-data-name" >message_sender</span> <i class="fa fa-circle me"></i></div><div class="message other-message float-right">'+ data.message +'</div></li>')
    };




  chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};


    $('#chat-message-submit').click(function(e){
      var message=$('#send_message').val()
      chatSocket.send(JSON.stringify({
        'message': message
      }));
    })
   

    },
    error:function(){
      console.log('error')
    }
  })
})

})


  
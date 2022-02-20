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


function send_message(socketname,data){
  socketname.send(JSON.stringify(data))
}

$('.link_room').click(function(e){
  e.preventDefault()
  $('.chat-message-list').html('')
  let target=$(this).attr('target')
  $.ajax({
    type:'GET',
    url:'chat/'+target,
    data:{'room_name':target},
    success:function(res){
      let current_user=res.current_user
      $('.chat-with').html(res.room_name)
      $('.members').html('')
      for (i=res.members.length-1;i>=0;i--){ 
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
      var data={
        'command':'fetch_message',
        'room_name':target
      }
      send_message(chatSocket,data)
    }


    chatSocket.onmessage = function(e) {
      const databox = JSON.parse(e.data);
      const data=databox.message
      for(i=data.length-1;i>=0;i--){
        if(data[i].__str__==current_user){
          $('.chat-message-list').append('<li class="clearfix"><div class="message-data align-right"><span class="message-data-time" >'+ data[i].message_send_time +'</span> &nbsp; &nbsp;<span class="message-data-name" >'+ data[i].__str__ +'</span> <i class="fa fa-circle "></i></div><div class="message other-message  float-right">'+ data[i].content +'</div></li>')
        }
        else{
          $('.chat-message-list').append('<li class="clearfix"><div class="message-data "><span class="message-data-time" >'+ data[i].message_send_time +'</span> &nbsp; &nbsp;<span class="message-data-name" >'+ data[i].__str__ +'</span> <i class="fa fa-circle me"></i></div><div class="message my-message  float-right">'+ data[i].content +'</div></li>')
        }
      }
      // console.log(databox)
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


  
var me = {};
me.avatar = "../static/User.png";

var you = {};
you.avatar = "../static/Bot.png";

var flag = 0;

var ctr = '';

ctr = '<li class="message left appeared">'+
       '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ you.avatar +'" /> </div>'+
       '<div class="text_wrapper">'+
       '<div class="text">Welcome to Twitter Bot. Please choose one option.'+'<br><br>'+
       '<button type="submit" id="select_by_keyword"> Search by keyword </button>'+'<br><br>'+
       '<button type="submit" id="select_by_account"> Search by username </button>'+
	   '</div>'+
       '</li>';
$("#ul_input").append(ctr).scrollTop($("#ul_input").prop('scrollHeight'));

function insert_chat(who,text){
	var control = '';
	if (who == 'me') {
		control = '<li class="message right appeared">'+
	                '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ me.avatar +'" /> </div>'+
	                '<div class="text_wrapper">'+
	                '<div class="text">'+text+'</div>'+
	                '</div>'+
	                '</li>';
	}
	else {
		control = '<li class="message left appeared">'+
	                '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ you.avatar +'" /> </div>'+
	                '<div class="text_wrapper">'+
	                '<div class="text">'+text+'</div>'+
	                '</div>'+
	                '</li>';
	}
	setTimeout(
	      function(){                        
	          $("#ul_input").append(control).scrollTop($("#ul_input").prop('scrollHeight'));
	      });
}

function insert_menu(command) {
	var control = '';
	if(command == 'return') {
		control = '<li class="message left appeared">'+
                    '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ you.avatar +'" /> </div>'+
                    '<div class="text_wrapper">'+
                    '<button type="submit" id="select_by_keyword"> Search by keyword </button>'+'<br><br>'+
                    '<button type="submit" id="select_by_account"> Search by username </button>'+
	                '</div>'+
                    '</li>';
	}
	setTimeout(
	      function(){                        
	          $("#ul_input").append(control).scrollTop($("#ul_input").prop('scrollHeight'));
	      });
}

 $(document).on('click', '#select_by_keyword',function(){
	var element = document.getElementById("select_by_keyword");
	var text = element.innerText;
	insert_chat("me", text);
	insert_chat("you", "Please input a keyword.");
	flag = 1;
});


 $(document).on('click', '#select_by_account',function(){
	var element = document.getElementById("select_by_account");
	var text = element.innerText;
	insert_chat("me", text);
	insert_chat("you", "Please input the username.");
	flag = 2;
});


function interact(message){
	console.log("STARTING");
	$.ajax({
	  type: 'POST',
	  url: '/reply',
	  contentType: 'application/json',
	  dataType: 'json',
	  data: message,
	 success: function(data){
		insert_chat("you",data['text']);
	 }
	  });
}

var tweet_text = "";

function get_message(){
	var message = document.getElementById("text_message").value;
	var json_data = {"msg":message};
	var sender = JSON.stringify(json_data);
	var getElement = document.getElementById("text_message");
	getElement.innerText = "";
	getElement.value = "";
	getElement.text = "";
	console.log(sender);
	console.log(message);
	insert_chat('me',message);
	if(message=='return'){
		insert_menu('return');
	}
	else{
		if(flag == 1) {
			console.log("STARTING");
			times = []
			tweets = []
			$.ajax({
				type: 'POST',
				url: '/tweetDisplayByKeyword',
				contentType: 'application/json',
				dataType: 'json',
				data: sender,
				success: function(data){
					times = data['time'];
					tweets = data['text'];
					for(var i = 0; i < tweets.length; i++) {
						tweet_text = tweet_text + times[i];
						tweet_text = tweet_text + "   ";
						tweet_text = tweet_text + tweets[i];
						tweet_text = tweet_text + '\r\n';
					}
					insert_chat("you", tweet_text);
			 	}
			});
		}
		else if(flag == 2) {
			console.log("STARTING");
			times = []
			tweets = []
			$.ajax({
				type: 'POST',
				url: '/tweetDisplayByAccount',
				contentType: 'application/json',
				dataType: 'json',
				data: sender,
				success: function(data){
					times = data['time'];
					tweets = data['text'];
					for(var i = 0; i < tweets.length; i++) {
						tweet_text = tweet_text + times[i];
						tweet_text = tweet_text + "   ";
						tweet_text = tweet_text + tweets[i];
						tweet_text = tweet_text + '\r\n';
					}
					insert_chat("you", tweet_text);
			 	}
			});
		}
		else {
			interact(sender);
		}
		flag = 0;
	}
 }



css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.bot .avatar {
  background-color: #2b313e;
}
.user .avatar {
  background-color: #475063;
}

.chat-message .avatar {
  width: 60px;
  height: 30px;
  padding:0px 5px;
  border-radius : 5px;
  text-align: center;
}


.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        Bot
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
# <img src="https://ibb.co/Ptn1HKT" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        Human
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
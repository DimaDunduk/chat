@channel_session_user
def loadhistory_receive(message):
    data = json.loads(message['text'])
    chat_queryset = ChatMessage.objects.filter(id__lte=data['last_message_id']).order_by("-created")[:10]
    chat_message_count = len(chat_queryset)
    if chat_message_count > 0:
        first_message_id = chat_queryset[len(chat_queryset)-1].id
    else:
        first_message_id = -1
    previous_id = -1
    if first_message_id != -1:
        try:
            previous_id = ChatMessage.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
        except IndexError:
            previous_id = -1
 
    chat_messages = reversed(chat_queryset)
    cleaned_chat_messages = list()
    for item in chat_messages:
        current_message = item.message_html
        cleaned_item = {'user' : item.user.username, 'message' : current_message }
        cleaned_chat_messages.append(cleaned_item)
 
    my_dict = { 'messages' : cleaned_chat_messages, 'previous_id' : previous_id }
    message.reply_channel.send({'text': json.dumps(my_dict)})
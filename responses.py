def response_handler(message) -> str:
    pr_message = message.lower()
    if pr_message == "nino":
        return "123"
    if pr_message == "intellectual":
        return "If you want to get an 'Intellectual role' you will have to PLAY 10 DOTA GAMES WITH NINO EVERY DAY FOR A WEEK"
    if pr_message == "!div":
        return "<@204295265023164416> <@277458944727842827> <@248483763804307456> IT'S TIME <:LETSGO:1114624389384785960>"
    else:
        pass


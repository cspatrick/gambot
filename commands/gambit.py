import requests, discord, os
from datetime import datetime

#email: ""
#password: ""
#recaptchaToken: ""


def profit(num):

    games_list = ['Basketball', 'Ice Hockey', 'Baseball', 'Esports']
    auth_token = os.environ.get('AUTH_TOKEN')
    headers = {'Authorization': auth_token}

    response = requests.get(
        'https://api-production.gambitrewards.com/api/v1/matches/', headers=headers)

    #webhook = discord.Webhook.from_url('', adapter=discord.RequestsWebhookAdapter())

    match_ids = []
    for match in response.json()['items']:
        if match['sport_category']['sport']['name'] != 'Soccer':
            match_ids.append(match['id'])

    if not match_ids:
        return discord.Embed(description='No current games.', color=242424)

    x = 0
    y = 0
    odds1 = 0
    odds2 = 0
    tokens = num
    profit = 0

    max_profit = 0
    profit_id = ''
    profit_name = ''
    profit_odds1 = 0
    profit_odds2 = 0
    bet1 = 0
    bet2 = 0

    prev_profit = 0
    prev_profit_id = ''
    prev_profit_name = ''
    prev_profit_odds1 = 0
    prev_profit_odds2 = 0
    prev_bet1 = 0
    prev_bet2 = 0

    max_profit2 = 0
    profit_id2 = ''
    profit_name2 = ''
    profit_odds12 = 0
    profit_odds22 = 0
    bet12 = 0
    bet22 = 0

    for id in match_ids:
        response2 = requests.get(
            'https://api-production.gambitrewards.com/api/v1/matches/' + id, headers=headers)
        for bet in response2.json()['item']['bet_types_matches']:
            if bet['bet_type']['label'] == 'Pick the Winner':
                odds1 = bet['match_lines'][0]['payout']
                odds2 = bet['match_lines'][1]['payout']
                x = tokens / (1+odds1/odds2)
                y = tokens / (1+odds2/odds1)
                profit = (odds1*x - tokens*.95) / (tokens*.95)
                if profit > max_profit:
                    prev_profit = max_profit
                    prev_profit_id = profit_id
                    prev_profit_name = profit_name
                    prev_profit_odds1 = profit_odds1
                    prev_profit_odds2 = profit_odds2
                    prev_bet1 = bet1
                    prev_bet2 = bet2
                    max_profit = profit
                    profit_id = id
                    profit_name = response2.json()['item']['name']  + " " + datetime.fromisoformat(response2.json()['item']['cut_off_time'].replace("Z", "")).strftime("%x")
                    profit_odds1 = odds1
                    profit_odds2 = odds2
                    bet1 = x
                    bet2 = y
                if (profit > max_profit2) and (id is not profit_id):
                    max_profit2 = profit
                    profit_id2 = id
                    profit_name2 = response2.json()['item']['name']  + " " + datetime.fromisoformat(response2.json()['item']['cut_off_time'].replace("Z", "")).strftime("%x")
                    profit_odds12 = odds1
                    profit_odds22 = odds2
                    bet12 = x
                    bet22 = y
                if (prev_profit > max_profit2) and (prev_profit_id is not profit_id):
                    max_profit2 = prev_profit
                    profit_id2 = prev_profit_id
                    profit_name2 = prev_profit_name
                    profit_odds12 = prev_profit_odds1
                    profit_odds22 = prev_profit_odds2
                    bet12 = prev_bet1
                    bet22 = prev_bet2

    embed = discord.Embed(title='Gambit Profit', color=242424)
    embed.add_field(
        name='Game', value='[{}](https://app.gambitrewards.com/match/{})'.format(profit_name, profit_id), inline=False)
    embed.add_field(name='Odds 1', value=str(profit_odds1))
    embed.add_field(name='Odds 2', value=str(profit_odds2))
    embed.add_field(name='Profit', value=format(max_profit, '.2%'))
    embed.add_field(name='Bet 1', value=str(round(bet1)))
    embed.add_field(name='Bet 2', value=str(round(bet2)))
    embed.add_field(name='Tokens', value=tokens)

    embed.add_field(
        name='Game', value='[{}](https://app.gambitrewards.com/match/{})'.format(profit_name2, profit_id2), inline=False)
    embed.add_field(name='Odds 1', value=str(profit_odds12))
    embed.add_field(name='Odds 2', value=str(profit_odds22))
    embed.add_field(name='Profit', value=format(max_profit2, '.2%'))
    embed.add_field(name='Bet 1', value=str(round(bet12)))
    embed.add_field(name='Bet 2', value=str(round(bet22)))
    embed.add_field(name='Tokens', value=tokens)
    embed.set_footer(text='Swagit donations accepted @kirtap')
    #webhook.send(embed=embed, content='<@&{}>'.format('526067036145844235'))
    # print('Best hedge is '+profit_name+' at '+str(profit_odds1)+'/'+str(profit_odds2) +
    #      ' '+format(max_profit, '.2%')+'\nhttps://app.gambitrewards.com/match/'+profit_id)
    return embed


#profit(20000)

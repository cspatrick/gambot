from pydoc import describe
import requests
import discord

#email: ""
#password: ""
#recaptchaToken: ""


def profit(*args):

    games_list = ['Basketball', 'Ice Hockey', 'Baseball']
    auth_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTQxMDg5MjMsInN1YiI6ImJkZDAyNzU3LTdiNDQtNDg4MC1hOGE3LTFlNWUyZWFhNWQxNSJ9.p_E162Hi1H_l73_v_o5YqTu_q4uYc1AaBILHAvpCV6I'
    if args[1]:
        auth_token = args[1]
    headers = {'Authorization': auth_token}

    response = requests.get(
        'https://api-production.gambitrewards.com/api/v1/matches/', headers=headers)

    #webhook = discord.Webhook.from_url('https://discord.com/api/webhooks/650101895343505418/xt-j3QlTmgaVfNGc2iwKs_EOrlA4VYb-PmCf84_EvZl98R0dGfy5x8friwqej08Shw7z', adapter=discord.RequestsWebhookAdapter())

    match_ids = []
    for match in response.json()['items']:
        if match['sport_category']['sport']['name'] in games_list:
            match_ids.append(match['id'])

    if not match_ids:
        return discord.Embed(description='No current games.', color=242424)

    x = 0
    y = 0
    odds1 = 0
    odds2 = 0
    tokens = args[0]
    profit = 0
    max_profit = 0
    profit_id = ''
    profit_name = ''
    profit_odds1 = 0
    profit_odds2 = 0

    for id in match_ids:
        response2 = requests.get(
            'https://api-production.gambitrewards.com/api/v1/matches/' + id, headers=headers)
        for bet in response2.json()['item']['bet_types_matches']:
            if bet['bet_type']['label'] == 'Pick the Winner':
                odds1 = bet['match_lines'][0]['payout']
                odds2 = bet['match_lines'][1]['payout']
                x = tokens / (1+odds1/odds2)
                y = tokens / (1+odds2/odds1)
                profit = (odds1*x - tokens*.9) / (tokens*.9)
                if profit > max_profit:
                    max_profit = profit
                    profit_id = id
                    profit_name = response2.json()['item']['name']
                    profit_odds1 = odds1
                    profit_odds2 = odds2

    embed = discord.Embed(title='Gambit Profit', color=242424)
    embed.add_field(
        name='Game', value='[{}](https://app.gambitrewards.com/match/{})'.format(profit_name, profit_id), inline=False)
    embed.add_field(name='Odds 1', value=str(profit_odds1))
    embed.add_field(name='Odds 2', value=str(profit_odds2))
    embed.add_field(name='Profit', value=format(max_profit, '.2%'))
    embed.add_field(name='Bet 1', value=str(round(x)))
    embed.add_field(name='Bet 2', value=str(round(y)))
    embed.add_field(name='Tokens', value=tokens)
    embed.set_footer(text='Swagit donations accepted @phillter')
    #webhook.send(embed=embed, content='<@&{}>'.format('526067036145844235'))
    #print('Best hedge is '+profit_name+' at '+str(profit_odds1)+'/'+str(profit_odds2) +
    #      ' '+format(max_profit, '.2%')+'\nhttps://app.gambitrewards.com/match/'+profit_id)
    return embed
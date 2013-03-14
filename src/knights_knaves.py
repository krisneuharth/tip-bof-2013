"""
Knights and Knaves
"""


class Actor(object):
    abstract = True

    def __init__(self, n):
        self.name = n

    def __repr__(self):
        cls = self.__class__.__name__
        return '%s - %s' % (cls, self.name)

    def query(self, q):
        """
        Receive a query, respond
        """

        r = self.conjure_response(q)
        return self.respond(r)

    def respond(self, r):
        return r

    def conjure_response(self, q):
        raise NotImplemented

    def tell_truth(self):
        raise NotImplemented


class Knight(Actor):
    """
    Knight
    """

    def conjure_response(self, q):
        """
        Naive response
        """

        return u'We are of the same kind.'

    def tell_truth(self):
        """
        Knights always tell the truth
        """

        return True


class Knave(Actor):
    """
    Knave
    """

    def conjure_response(self, q):
        """
        Naive response
        """

        return u'We are of different kinds.'

    def tell_truth(self):
        """
        Knaves always lie
        """

        return False


class Game(object):
    """
    Simple game object to tell the story
    """

    def __init__(self):
        """
        Populate the game with actors
        """

        self.actors = []
        self.actors.append(Knight('John'))
        self.actors.append(Knave('Bill'))

    def play(self):
        """
        Play the game
        """

        print '''
          _____ _   _ _____    ____ _____ ___  ______   __
         |_   _| | | | ____|  / ___|_   _/ _ \|  _ \ \ / /
           | | | |_| |  _|    \___ \ | || | | | |_) \ V /
           | | |  _  | |___    ___) || || |_| |  _ < | |    _   _   _
           |_| |_| |_|_____|  |____/ |_| \___/|_| \_\|_|   (_) (_) (_)

        '''


        print u'\nAs luck would have it, your plane has crashed and you now find yourself stranded on an island.\n'

        print u'\nOn this island, all inhabitants are either knights, who always tell the truth, or knaves, who always lie.\n'

        print u'\nHow do you know this?'
        raw_input('<press a key>\n')

        print u'\nWikipedia, of course.'
        raw_input('<press a key>\n')

        print u'\nSo, looking for help, you wander around aimlessly and to your surprise you encounter two odd fellows.\n'

        print u'\nThey eagerly welcome you to their island, and offer their names, John and Bill.\n'

        print u'\nKnowing what you know, and also knowing who not to trust with your life, you politely turn to each one of them and ask...'
        raw_input('<press a key>\n')

        for q in [u'"What kind are you?"']:
            for actor in self.actors:
                print q
                r = actor.query(q)
                print u'%s: %s' % (actor.name, r)

        print u'\nThese men certainly are odd and surely you can outsmart them.'
        raw_input('<press a key>\n')

        answers = ['t', 't']

        # Question #1
        while True:
            r = raw_input("Is John a Knave (t/f)?  ").strip()
            if str(r) == answers[0]:
                print 'Correct!\n'
                break
            else:
                print 'Try again!\n'
                continue

        # Question #2
        while True:
            r = raw_input("Is Bill a Knight (t/f)?  ").strip()
            if str(r) == answers[1]:
                print 'Correct!\n'
                break
            else:
                print 'Try again!\n'
                continue

        print u'\nClearly there is no fooling you! You quickly befriend John and...'
        raw_input('<press a key>\n')

        print """

                                   `:--://:-`
                                     ::::.:::-
                                      /--/-+:+`
                                `....:/-.-```-/
                                --..`````````.:
                                 `/.``````o`:/:
                                 .-`:`````:`..-.
                                 /```:`````````:
                               `--````::````./:+`
  `.......................-...-:```````.--.``.+/.
   .--```-````````````````````````````.-`:/o+o+s`
     /````````````````````````````````.``:`-..-
    :```````````````````````````````.````:
   :```````````````````````````````.````:`
   :```````````````````````````````````-`
   :`````````````````````````````````-:`
   /````````````.`````````````````.:+.
   .-```````-``:```````````-`````-`+
    -.```````:+-.........../.````:`-.
    `:````.-./             /`````/``:
    --````:``.-            .-`````:/+
      :.```--``:            hmhsyNd:`
       /````.sss
       `syyyo/


        """

        print u'\nYou are eaten by a goat!'
        raw_input('<press a key>\n')

        print u'\nWhile this island is largely inhabited by knights and knaves, you obviously neglected the part on the wiki page about the carnivorous goats.'
        raw_input('<press a key>\n')

        print u'\nNext time maybe pay more attention?\n'

        print '''
              _____ _   _ _____   _____ _   _ ____  _
             |_   _| | | | ____| | ____| \ | |  _ \| |
               | | | |_| |  _|   |  _| |  \| | | | | |
               | | |  _  | |___  | |___| |\  | |_| |_|
               |_| |_| |_|_____| |_____|_| \_|____/(_)
        '''


if __name__ == "__main__":
    #
    # Driver
    #

    game = Game()
    game.play()

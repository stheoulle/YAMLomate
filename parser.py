class YAMLParser:
    def __init__(self):
        # Initialisation de la pile pour les états et les tabs
        self.stack = []  # Pour la logique principale
        self.tab_stack = []  # Pour compter les tabulations (multiples de 3 espaces)
        self.previous_tab_count = 0  # Variable pour garder le précédent nombre de tabs

    def parse(self, input_data):
        # Initialisation de l'état et de la position dans le fichier
        current_state = 1
        position = 0
        length = len(input_data)

        # Boucle tant qu'on n'est pas arrivé à la fin du fichier
        while position < length:
            char = input_data[position]

            if current_state == 1:
                # Transition pour détecter un tiret ou un autre caractère
                if char == "-":
                    current_state = 2
                else:
                    current_state = 5

            elif current_state == 2:
                if char == "-":
                    current_state = 3
                elif char == " ":
                    position += 1  # Ignorer l'espace après le tiret
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and state {current_state}")

            elif current_state == 3:
                if char == "-":
                    current_state = 4
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and state {current_state}")

            elif current_state == 4:
                if char == "\n":
                    current_state = 5
                elif char == " ":
                    position += 1  # Ignorer l'espace après un élément traité
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and state {current_state}")

            elif current_state == 5:
                # Gestion des commentaires, scalaires et tabs
                if char == "#":
                    current_state = 6
                elif char.isalnum() or char in "_ /.,`":
                    current_state = 7
                elif char == ":":
                    current_state = 8
                elif char == "." and input_data[position:position+3] == "...":
                    current_state = 15
                    position += 2  # Sauter les deux caractères supplémentaires
                elif char == "\n":
                    position += 1  # Avancer pour gérer les sauts de ligne
                    position = self._handle_tab_logic(input_data, position)
                elif char == " ":
                    position += 1  # Ignorer les espaces en général
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and state {current_state}")

            elif current_state == 6:
                # Commentaire : tout ignorer jusqu'à la fin de la ligne
                if char == "\n":
                    current_state = 5
                else:
                    current_state = 6  # Continuer à traiter le commentaire

            elif current_state == 7:
                if char == ":":
                    current_state = 8
                elif char.isalnum() or char in "_-/.,'":
                    current_state = 7
                elif char == "\n":
                    position += 1  # Avancer pour gérer les sauts de ligne
                    position = self._handle_tab_logic(input_data, position)
                elif char == "#":
                    current_state = 6
                elif char == " ":
                    position += 1  # Ignorer les espaces dans les scalaires
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and state {current_state}")

            elif current_state == 8:
                if char == "|":
                    current_state = 9
                elif char == ">":
                    current_state = 9
                elif char == "\n":
                    current_state = 5
                    position = self._handle_tab_logic(input_data, position)

                elif char == "#":
                    current_state = 6
                elif char.isalnum() or char in " _-.:\"'/+=[}]{`":
                    current_state = 8
                elif char == " ":
                    position += 1  # Ignorer les espaces après un deux-points
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and state {current_state}")

            elif current_state == 9:
                if char == "\n":
                    current_state = 10
                else:
                    current_state = 9  # Continuation d'un bloc de texte

            elif current_state == 10:
                if char == " ":
                    current_state = 11
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and state {current_state}")

            elif current_state == 11:
                if char.isalnum() or char in " _-.:\"'/":
                    current_state = 11
                elif char == "\n":
                    current_state = 5
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and state {current_state}")

            elif current_state == 15:
                return True

            # Gestion de la fin de fichier
            if position == length - 1:
                if current_state in {5, 1}:
                    break
                else:
                    raise SyntaxError(f"Unexpected EOF at position {position} and current_state {current_state}")

            position += 1

        return True  # Si tout est conforme

    def _handle_tab_logic(self, input_data, position):
        """
        Gestion des tabs (multiples de 3 espaces).
        """
        tab_count = 0
        length = len(input_data)

        while position < length and input_data[position] == " ":
            tab_count += 1
            position += 1

        # Vérification si c'est un multiple de 3
        if tab_count % 3 != 0:
            raise SyntaxError(f"Invalid tab spacing at position {position}")

        # Calcul du nombre de tabs
        current_tab_count = tab_count // 3

        # Vérification de la transition d'indentation
        if current_tab_count > self.previous_tab_count + 1:
            raise SyntaxError(f"Indentation too deep at position {position}")
        elif current_tab_count < 0:
            raise SyntaxError(f"Unexpected negative indentation at position {position}")

        # Mise à jour de l'état d'indentation
        self.previous_tab_count = current_tab_count

        # Mise à jour de la pile des tabs (on garde une trace utile pour des scénarios plus complexes)
        if current_tab_count == 0:
            self.tab_stack.clear()  # Si on retourne au niveau racine, la pile est réinitialisée
        else:
            while self.tab_stack and self.tab_stack[-1] > current_tab_count:
                self.tab_stack.pop()  # Retirer les niveaux plus profonds que l'indentation actuelle

        self.tab_stack.append(current_tab_count)
        return position


# Exemple d'utilisation :

yaml_input ="""apiVersion: apps/v1
kind: Deployment
metadata:
   name: redis-follower-deployment
   labels:
      app: redis
spec:
   selector:
      matchLabels:
         app: redis
         role: follower
         tier: backend
   replicas: 1
   template:
      metadata:
         labels:
            app: redis
            role: follower
            tier: backend
      spec:
         containers:
         -  name: follower
            image: gcr.io/google_samples/gb-redis-follower:v2
            resources:
               requests:
                  cpu: 100m
                  memory: 100Mi
            env:
            -  name: GET_HOSTS_FROM
               value: dns
            ports:
            -  containerPort: 6379
            volumeMounts:
            -  name: redis-follower-data
               mountPath: /data
         volumes:
         -  name: redis-follower-data
            persistentVolumeClaim:
               claimName: redis-follower-pvc

"""

yaml_input_2="""# Un exemple complet pour tester l'automate

key1: value1  # Une clé avec une valeur simple
key2:          # Une clé avec une valeur complexe
   - list_item1
   - list_item2
   - list_item3: embedded_value

key3: >        # Un bloc plié
  Ceci est un bloc de texte plié.
  La deuxième ligne est collée à la première.

key4: |        # Un bloc littéral
  Ceci est un bloc de texte littéral.
  La deuxième ligne reste séparée.

key5:          # Une clé avec sous-objets
  subkey1: value1
  subkey2: value2
  subkey3:
   - list_item1
   - list_item2
   - list_item3

# Test d'une clé avec des caractères spéciaux autorisés
key_with_special_chars: "valeur-123_./`"

# Un test de fin de document
...
"""

parser = YAMLParser()
try:
    if parser.parse(yaml_input):
        print("Le YAML est conforme.")
except SyntaxError as e:
    print(f"Erreur de syntaxe : {e}")

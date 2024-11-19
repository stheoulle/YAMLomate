class YAMLParser:
    def __init__(self):
        # Initialisation de la pile
        self.stack = []
        self.tab_stack = []

    def parse(self, input_data):
        # Initialisation de l'état et de la position dans le fichier
        current_state = 1
        position = 0
        length = len(input_data)

        # Boucle tant qu'on n'est pas arrivé à la fin du fichier
        while position < length:
            char = input_data[position]

            # Gestion des transitions selon l'état de l'automate
            if current_state == 1:
                if char == "-":
                    current_state = 2
                else:
                    current_state = 5

            elif current_state == 2:
                if char == "-":
                    current_state = 3
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state}")

            elif current_state == 3:
                if char == "-":
                    current_state = 4
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state}")

            elif current_state == 4:
                if char == "\n":
                    current_state = 5
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state}")

            elif current_state == 5:
                if char == "#":
                    current_state = 6
                elif char == "." and input_data[position+1] == "." and input_data[position+2] ==".":
                    current_state = 15
                elif char == "-":
                    current_state = 5  # Rester dans le même état si tiret
                elif char == "\n":
                    current_state = 5  # Rester dans le même état si saut de ligne
                
                elif char.isalnum() or char == "_" or char == " ":  # Vérification d'un scalaire
                    # Scalaire trouvé, on passe à l'état 7 et on vérifie le caractère suivant (peek tab)
                    current_state = 7
                    # Effectuer un peek pour voir si le caractère suivant est un tab
                    if position + 1 < length:
                        next_char = input_data[position + 1]
                        # if next_char == "\t":
                        #     current_state = 7  # Si tabulation, rester dans l'état 7
                        # else:
                        #     raise SyntaxError(f"Unexpected character '{next_char}' after scalar at position {position + 1}")
                    else:
                        break
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state} next is {input_data[position+1]}")



            elif current_state == 6:
                if char == "\n":
                    current_state = 5
                elif char.isalnum() or char == "_" or char == " " or char == "-" or char == "(" or char == ")" or char == "." or char == "'" or char == '"' or char == ',' or char =="/":  # Vérification d'un scalaire
                    current_state = 6 
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state}")

            elif current_state == 7:
                if char == ":":
                    current_state = 8
                elif char.isalnum() or char == "_" or char == "-" or char == "/" :  # Vérification d'un scalaire
                    current_state = 7  # Rester dans l'état 7 si c'est un scalaire
                elif char == "\n":
                    current_state = 5  # Revenir à l'état 5 sur un saut de ligne
                elif char == " ":
                    current_state = 7  # Revenir à l'état 5 sur un saut de ligne
                elif char == "#":
                    current_state = 6  # Revenir à l'état 5 sur un saut de ligne
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state}")

            elif current_state == 8:
                # Gestion du saut de ligne suivi d'un espace ou autre caractère valide
                if char == "\n":
                    if position + 1 < length and input_data[position + 1] in [' ', '\t', '-', '\n']:  # Vérifier le caractère suivant
                        current_state = 8  # Rester dans l'état 8 si le caractère suivant est valide
                    else:
                        current_state = 5  # Revenir à l'état 5 si le caractère suivant est inattendu
                elif char == ":":
                    current_state = 8  # Rester dans l'état 8 si on rencontre un ':'
                elif char == "|":
                    current_state = 9  # Passer à l'état 9 si on rencontre '|'
                elif char == ">":
                    current_state = 9  # Passer à l'état 9 si on rencontre '>'
                elif char.isalnum() or char == "_" or char == " " or char == "-" or char == "(" or char == ")" or char == "." or char == "'" or char == '"' or char == "/" or char =="#" or char == ',' or char =="/" or char =="+" or char =="[" or char =="]" or char =="`":  # Vérification d'un scalaire
                    current_state = 8  # Rester dans l'état 8 si c'est un scalaire
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current state is {current_state} ")

            elif current_state == 9:
                if char == "\n":
                    current_state = 10
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state}")

            elif current_state == 10:
                if char == " ":
                    current_state = 11
                elif char == ".":
                    self.stack.append("block")
                    current_state = 11
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state}")

            elif current_state == 11:
                if char == "\n" and position + 1 < length:
                    if input_data[position+1] != " ":
                        current_state = 5
                if char == "\n" and position + 1 == length:
                    current_state = 5
                elif char == "\n" and position + 1 < length:
                    if input_data[position+1] == " ":
                        current_state = 10
                elif char.isalnum() or char == "_" or char == " " or char == "-" or char == "(" or char == ")" or char == "." or char == "'" or char == '"' or char == '/' or char =="#" or char == ',' or char =="/" or char =="+" :  # Vérification d'un scalaire
                    current_state == 11
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state}")

            elif current_state == 12:
                if char == "\n":
                    current_state = 5  # Transition vers l'état 5 après un saut de ligne
                else:
                    raise SyntaxError(f"Unexpected character '{char}' at position {position} and current_state {current_state}")

           
            elif current_state == 15:
                return True

            # Gestion de la fin de fichier (EOF)
            if position == length - 1:
                if current_state == 5 or current_state == 1:
                    break
                else:
                    # Si l'analyse se termine dans un état invalide, lever une erreur
                    raise SyntaxError(f"Unexpected EOF, expected state 15 at position {position} and current_state {current_state}")

            position += 1  # Passer au caractère suivant

        return True  # Si on arrive ici, le YAML est conforme

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
      - name: follower
        image: gcr.io/google_samples/gb-redis-follower:v2
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
        env:
        - name: GET_HOSTS_FROM
          value: dns
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-follower-data
          mountPath: /data
      volumes: 
      - name: redis-follower-data
        persistentVolumeClaim:
          claimName: redis-follower-pvc
"""

yaml_input2="""Building Microservices:
    author: Sam Newman
    language: English
    publication-year: 2021
    pages: 586
"""
yaml_input3="""# This is a single line comment
foo: bar # this is an inline comment
"""

yaml_input4="""# This is a float scalar
pi: 3.14 

# This is also a float scalar
area: 19.625

# And yet another scalar, in scientific notation
mass: 1.67e-27

"""

yaml_input5="""# A block sequence of strings
fruits:
  - apple
  - banana
  - cherry

# A block sequence of dictionaries
users:
  - name: Alice
    age: 35
    hobbies:
      - reading
      - writing
      - horseback riding
  - name: Bob
    age: 33
    hobbies:
      - coding
      - gaming
      - miniature painting

"""

yaml_input6="""# These are true/false boolean scalars
active: true
enabled: false

# These are yes/no boolean scalars
email-consent: yes
sms-consent: no

# These are on/off boolean scalars
switch: on
light: off

"""

yaml_input_final="""# SCALAR TYPES

# Our root object will be a map
key: value
another-key: another string value that goes on and on
a-number-value: 100
a-number-in-scientific-notation: 1e+12
a-hex-value: 0x123 # this will evaluate to 291
an-octal-value: 0123 # this will evaluate to 83

# And now some boolean values
booleanTrue: true
booleanFalse: false

yesValue: yes # this evaluates to true
noValue: no # this will evaluate to false

# Strings don't need to be quoted but they can be
a-simple-string: Does not require quotes
single-quotes: 'have ''one'' escape pattern'

# Multiple-line strings can be written as a literal block
literal_block: |
  This entire block of text will have
  its value preserved
  with line breaks being preserved

  The literal continues until de-dented and the leading indentation is
  stripped

# Or in a folded block
folded_style: >
  This entire block of text will have its values preserved with line
  breaks being converted into spaces

  Blank lines like above are converted to a newline character

      More-indented lines keep their newlines too -
      this text will appear over two lines

# COLLECTION TYPES

# Nesting uses indentation Better use 2 space indent
a_nested_map:
  key: value
  another_key: Another Value
  another_nested_map:
    hello: world


# Sequences look like this
a_sequence:
  - Item 1
  - Item 2
  - 0.5
  - Item 4
  - key: value
    another_key: another_value
  - - This is a sequence
    - inside another sequence
  - - - Sequence-ception
"""

yaml_input_final2="""apiVersion: claudie.io/v1beta1
kind: InputManifest
metadata:
  name: ExampleManifest
  labels:
    app.kubernetes.io/part-of: claudie
spec:
  # Providers field is used for defining the providers. 
  # It is referencing a secret resource in Kubernetes cluster.
  # Each provider haves its own mandatory fields that are defined in the secret resource.
  # Every supported provider has an example in this input manifest.
  # providers:
  #   - name: 
  #       providerType:   # Type of the provider secret  
  #       secretRef:      # Secret reference specification.
  #         name:         # Name of the secret resource.
  #         namespace:    # Namespace of the secret resource.
  providers:
    # Hetzner DNS provider.
    - name: hetznerdns-1
      providerType: hetznerdns
      secretRef:
        name: hetznerdns-secret-1
        namespace: example-namespace

    # Cloudflare DNS provider.
    - name: cloudflare-1
      providerType: cloudflare
      secretRef:
        name: cloudflare-secret-1
        namespace: example-namespace

    # Hetzner Cloud provider.
    - name: hetzner-1
      providerType: hetzner
      secretRef:
        name: hetzner-secret-1
        namespace: example-namespace

    # GCP cloud provider.
    - name: gcp-1
      providerType: gcp
      secretRef:
        name: gcp-secret-1
        namespace: example-namespace

    # OCI cloud provider.
    - name: oci-1
      providerType: oci
      secretRef:
        name: oci-secret-1
        namespace: example-namespace

    # AWS cloud provider.
    - name: aws-1
      providerType: aws
      secretRef:
        name: aws-secret-1
        namespace: example-namespace

    # Azure cloud provider.
    - name: azure-1
      providerType: azure
      secretRef:
        name: azure-secret-1
        namespace: example-namespace


  # Nodepools field is used for defining the nodepool specification.
  # You can think of them as a blueprints, not actual nodepools that will be created.
  nodePools:
    # Dynamic nodepools are created by Claudie, in one of the cloud providers specified.
    # Definition specification:
    # dynamic:
    #   - name:             # Name of the nodepool, which is used as a reference to it. Needs to be unique.
    #     providerSpec:     # Provider specification for this nodepool.
    #       name:           # Name of the provider instance, referencing one of the providers define above.
    #       region:         # Region of the nodepool.
    #       zone:           # Zone of the nodepool.
    #     count:            # Static number of nodes in this nodepool.
    #     serverType:       # Machine type of the nodes in this nodepool.
    #     image:            # OS image of the nodes in the nodepool.
    #     storageDiskSize:  # Disk size of the storage disk for compute nodepool. (optional)
    #     autoscaler:       # Autoscaler configuration. Mutually exclusive with Count.
    #       min:            # Minimum number of nodes in nodepool.
    #       max:            # Maximum number of nodes in nodepool.
    #     labels:           # Map of custom user defined labels for this nodepool. This field is optional and is ignored if used in Loadbalancer cluster. (optional)
    #     annotations:      # Map of user defined annotations, which will be applied on every node in the node pool. (optional)
    #     taints:           # Array of custom user defined taints for this nodepool. This field is optional and is ignored if used in Loadbalancer cluster. (optional)
    #       - key:          # The taint key to be applied to a node.
    #         value:        # The taint value corresponding to the taint key.
    #         effect:       # The effect of the taint on pods that do not tolerate the taint.
    #
    # Example definitions for each provider
    dynamic:
      - name: control-hetzner
        providerSpec:
          name: hetzner-1
          region: hel1
          zone: hel1-dc2
        count: 3
        serverType: cpx11
        image: ubuntu-22.04
        labels:
          country: finland
          city: helsinki
        annotations:
          node.longhorn.io/default-node-tags: '["finland"]'
        taints:
          - key: country
            value: finland
            effect: NoSchedule

      - name: compute-hetzner
        providerSpec:
          name: hetzner-1
          region: hel1
          zone: hel1-dc2
        count: 2
        serverType: cpx11
        image: ubuntu-22.04
        storageDiskSize: 50
        labels:
          country: finland
          city: helsinki
        annotations:
          node.longhorn.io/default-node-tags: '["finland"]'

      - name: compute-hetzner-autoscaled
        providerSpec:
          name: hetzner-1
          region: hel1
          zone: hel1-dc2
        serverType: cpx11
        image: ubuntu-22.04
        storageDiskSize: 50
        autoscaler:
          min: 1
          max: 5
        labels:
          country: finland
          city: helsinki
        annotations:
          node.longhorn.io/default-node-tags: '["finland"]'

      - name: control-gcp
        providerSpec:
          name: gcp-1
          region: europe-west1
          zone: europe-west1-c
        count: 3
        serverType: e2-medium
        image: ubuntu-os-cloud/ubuntu-2204-jammy-v20221206
        labels:
          country: germany
          city: frankfurt
        annotations:
          node.longhorn.io/default-node-tags: '["germany"]'

      - name: compute-gcp
        providerSpec:
          name: gcp-1
          region: europe-west1
          zone: europe-west1-c
        count: 2
        serverType: e2-small
        image: ubuntu-os-cloud/ubuntu-2204-jammy-v20221206
        storageDiskSize: 50
        labels:
          country: germany
          city: frankfurt
        taints:
          - key: city
            value: frankfurt
            effect: NoExecute
        annotations:
          node.longhorn.io/default-node-tags: '["germany"]'

      - name: control-oci
        providerSpec:
          name: oci-1
          region: eu-milan-1
          zone: hsVQ:EU-MILAN-1-AD-1
        count: 3
        serverType: VM.Standard2.1
        image: ocid1.image.oc1.eu-frankfurt-1.aaaaaaaavvsjwcjstxt4sb25na65yx6i34bzdy5oess3pkgwyfa4hxmzpqeq

      - name: compute-oci
        providerSpec:
          name: oci-1
          region: eu-milan-1
          zone: hsVQ:EU-MILAN-1-AD-1
        count: 2
        serverType: VM.Standard2.1
        image: ocid1.image.oc1.eu-frankfurt-1.aaaaaaaavvsjwcjstxt4sb25na65yx6i34bzdy5oess3pkgwyfa4hxmzpqeq
        storageDiskSize: 50

      - name: control-aws
        providerSpec:
          name: aws-1
          region: eu-central-1
          zone: eu-central-1c
        count: 2
        serverType: t3.medium
        image: ami-0965bd5ba4d59211c

      - name: compute-aws
        providerSpec:
          name: aws-1
          region: eu-central-1
          zone: eu-central-1c
        count: 2
        serverType: t3.medium
        image: ami-0965bd5ba4d59211c
        storageDiskSize: 50

      - name: control-azure
        providerSpec:
          name: azure-1
          region: West Europe
          zone: "1"
        count: 2
        serverType: Standard_B2s
        image: Canonical:0001-com-ubuntu-minimal-jammy:minimal-22_04-lts:22.04.202212120

      - name: compute-azure
        providerSpec:
          name: azure-1
          region: West Europe
          zone: "1"
        count: 2
        serverType: Standard_B2s
        image: Canonical:0001-com-ubuntu-minimal-jammy:minimal-22_04-lts:22.04.202212120
        storageDiskSize: 50

      - name: loadbalancer-1
        provider:
        providerSpec:
          name: gcp-1
          region: europe-west1
          zone: europe-west1-c
        count: 2
        serverType: e2-small
        image: ubuntu-os-cloud/ubuntu-2004-focal-v20220610

      - name: loadbalancer-2
        providerSpec:
          name: hetzner-1
          region: hel1
          zone: hel1-dc2
        count: 2
        serverType: cpx11
        image: ubuntu-20.04

    # Static nodepools are created by user beforehand.
    # In case you want to use them in the Kubernetes cluster, make sure they meet the requirements. https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin
    # Definition specification:
    # static:
    #   - name:             # Name of the nodepool, which is used as a reference to it. Needs to be unique.
    #     nodes:            # List of nodes which will be access under this nodepool.
    #       - endpoint:     # IP under which Claudie will access this node. Can be private as long as Claudie will be able to access it.
    #         secretRef:    # Secret reference specification, holding private key which will be used to SSH into the node (as root).
    #           name:       # Name of the secret resource.
    #           namespace:  # Namespace of the secret resource.
    #     labels:           # Map of custom user defined labels for this nodepool. This field is optional and is ignored if used in Loadbalancer cluster. (optional)
    #     annotations:      # Map of user defined annotations, which will be applied on every node in the node pool. (optional)
    #     taints:           # Array of custom user defined taints for this nodepool. This field is optional and is ignored if used in Loadbalancer cluster. (optional)
    #       - key:          # The taint key to be applied to a node.
    #         value:        # The taint value corresponding to the taint key.
    #         effect:       # The effect of the taint on pods that do not tolerate the taint.
    #
    # Example definitions
    static:
      - name: datacenter-1
        nodes:
          - endpoint: "192.168.10.1"
            secretRef:
              name: datacenter-1-key
              namespace: example-namespace

          - endpoint: "192.168.10.2"
            secretRef:
              name: datacenter-1-key
              namespace: example-namespace

          - endpoint: "192.168.10.3"
            secretRef:
              name: datacenter-1-key
              namespace: example-namespace
        labels:
          datacenter: datacenter-1
        annotations:
          node.longhorn.io/default-node-tags: '["datacenter-1"]'   
        taints:
          key: datacenter
          effect: NoExecute


  # Kubernetes field is used to define the kubernetes clusters.
  # Definition specification:
  #
  # clusters:
  #   - name:           # Name of the cluster. The name will be appended to the created node name.
  #     version:        # Kubernetes version in semver scheme, must be supported by KubeOne.
  #     network:        # Private network IP range.
  #     pools:          # Nodepool names which cluster will be composed of. User can reuse same nodepool specification on multiple clusters.
  #       control:      # List of nodepool names, which will be used as control nodes.
  #       compute:      # List of nodepool names, which will be used as compute nodes.
  #
  # Example definitions:
  kubernetes:
    clusters:
      - name: dev-cluster
        version: v1.26.13
        network: 192.168.2.0/24
        pools:
          control:
            - control-hetzner
            - control-gcp
          compute:
            - compute-hetzner
            - compute-gcp
            - compute-azure

      - name: prod-cluster
        version: v1.26.13
        network: 192.168.2.0/24
        pools:
          control:
            - control-hetzner
            - control-gcp
            - control-oci
            - control-aws
            - control-azure
          compute:
            - compute-hetzner
            - compute-gcp
            - compute-oci
            - compute-aws
            - compute-azure

      - name: hybrid-cluster
        version: v1.26.13
        network: 192.168.2.0/24
        pools:
          control:
            - datacenter-1
          compute:
            - compute-hetzner
            - compute-gcp
            - compute-azure

  # Loadbalancers field defines loadbalancers used for the kubernetes clusters and roles for the loadbalancers.
  # Definition specification for role:
  #
  # roles:
  #   - name:         # Name of the role, used as a reference later. Must be unique.
  #     protocol:     # Protocol, this role will use.
  #     port:         # Port, where traffic will be coming.
  #     targetPort:   # Port, where loadbalancer will forward traffic to.
  #     targetPools:  # Targeted nodes on kubernetes cluster. Specify a nodepool that is used in the targeted K8s cluster.
  #
  # Definition specification for loadbalancer:
  #
  # clusters:
  #   - name:         # Loadbalancer cluster name
  #     roles:        # List of role names this loadbalancer will fulfil.
  #     dns:          # DNS specification, where DNS records will be created.
  #       dnsZone:    # DNS zone name in your provider.
  #       provider:   # Provider name for the DNS.
  #       hostname:   # Hostname for the DNS record. Keep in mind the zone will be included automatically. If left empty the Claudie will create random hash as a hostname.
  #     targetedK8s:  # Name of the targeted kubernetes cluster
  #     pools:        # List of nodepool names used for loadbalancer
  #
  # Example definitions:
  loadBalancers:
    roles:
      - name: apiserver
        protocol: tcp
        port: 6443
        targetPort: 6443
        targetPools:
            - k8s-control-gcp # make sure that this nodepools is acutally used by the targeted `dev-cluster` cluster.
    clusters:
      - name: apiserver-lb-dev
        roles:
          - apiserver
        dns:
          dnsZone: dns-zone
          provider: hetznerdns-1
        targetedK8s: dev-cluster
        pools:
          - loadbalancer-1
      - name: apiserver-lb-prod
        roles:
          - apiserver
        dns:
          dnsZone: dns-zone
          provider: cloudflare-1
          hostname: my.fancy.url
        targetedK8s: prod-cluster
        pools:
          - loadbalancer-2
"""

parser = YAMLParser()
try:
    if parser.parse(yaml_input6):
        print("Le YAML est conforme.")
except SyntaxError as e:
    print(f"Erreur de syntaxe : {e}")

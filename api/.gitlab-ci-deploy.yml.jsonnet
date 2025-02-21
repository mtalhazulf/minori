local job(env) =
  {
    image: {
      name:"bitnami/kubectl",
     entrypoint: [""]
    },
    stage: "deploy",
    environment: {
      name: env
    },
    before_script: [
      "REGEX=\"^v([0-9]+\\.[0-9]+\\.[0-9]+)$\"",
      "VERSION=$(echo \"$CI_COMMIT_TAG\" | grep -qE \"${REGEX}\" && echo $(echo \"$CI_COMMIT_TAG\" | sed -E \"s|${REGEX}|\\1|\"))"
    ],
    script: [
      "kubectl --kubeconfig \"$KUBECONFIG\" -n $KUBE_NAMESPACE set image \"deployment/$KUBE_DEPLOYMENT\" \"$KUBE_DEPLOYMENT_CONTAINER\"=\"$CI_REGISTRY_IMAGE:$VERSION\""
    ]
  };

local enviroments = std.split(std.strReplace(std.extVar('enviroments'), "\n", " "), " ");
{
  ['deploy_' + enviroment]: job(enviroment)
  for enviroment in enviroments
}

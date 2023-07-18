def dostuff(): 
  if 'namespace' in app and app.namespace != '':
    namespace = app.namespace 
  else:
    namespace = (app.path | default('default') | basename) 


  repo_dir = ('cluster', app.path | default(''), app.name) | path_join 
  sources = [] 
  for source in app.sources:
    if 'chart' in source:
      (helm_repo,chart_name) = source.chart.split('/')
      source = {
          chart: chart_name,
          repoURL: helm_repositories[helm_repo],
          targetRevision: source.version,
          helm: {}
      }
      if 'skipCrds' in source:
        source.helm = { skipCrds: true }
      source.helm[valueFiles] = []
      if 'valueFiles' in source:
        for file in source.valueFiles:
          source.helm.valueFiles.push({{ ('$repo', repo_dir, file) | path_join }})
      else:
        source.helm.valueFiles.push({{ ('$repo', repo_dir, 'values.yaml') | path_join }})

  source = { 
    repoURL: {{ repo_url | default('https://github.com/clearlybaffled/dotfiles') }},
    path: repo_dir,
    targetRevision: branch
  }
  if ({{app.sources | map(attribute='chart')}}):
    source.ref = 'repo'
  if 'directory' in app:
    source[directory] = app.directory

  sources.push(source)

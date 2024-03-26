exec { 'killmenow':
  command     => '/usr/bin/pkill killmenow',
  path        => ['/bin', '/usr/bin'],
  onlyif      => '/usr/bin/pgrep -f killmenow',
  refreshonly => true,
}

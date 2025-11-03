ustor-iscsi login
ustor-iscsi enable-gateway
ustor-iscsi create-client test-client1 -i "iqn.test:client1" -a "192.168.1.100"
ustor-iscsi create-auth-group myAuthGroup -c 'user:admin secret:Passw0rd'
ustor-iscsi set-client-auth test-client1 -g 1 -at oneway

ustor-iscsi create-portal portalMy -a 192.168.88.23 -p 6230
ustor-iscsi export-iscsi myimage --portal-id 0 --lun-id 1 \
  --gateway ustvmmid1ldcn3.mindsw.dev --host-id 1

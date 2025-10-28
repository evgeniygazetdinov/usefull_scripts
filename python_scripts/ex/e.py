#!/usr/bin/env python3
"""
Script for creating complete iSCSI configuration from scratch
Creates: Gateway, Portal, Client (Initiator Group), Pool, Image and Export
"""

import argparse
import json
import sys
import time
from typing import Any, Dict, Optional

import requests


class ISCSISetupManager:
    """Manager for creating complete iSCSI configuration"""

    def __init__(
        self,
        base_url: str,
        username: str = "admin",
        password: str = "Passw0rd",
        verify_ssl: bool = False,
    ):
        """
        Initialize manager
        
        Args:
            base_url: Base API URL (e.g., http://localhost:8000)
            username: Username for authentication
            password: Password for authentication
            verify_ssl: Whether to verify SSL certificate
        """
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.token = None
        
        # Get token during initialization
        self._authenticate()

    def _authenticate(self) -> None:
        """
        Authentication and JWT token retrieval
        """
        try:
            url = f"{self.base_url}/api/proxy/auth/login"
            response = requests.post(
                url,
                data={"username": self.username, "password": self.password},
                verify=self.verify_ssl,
                timeout=None,  # No timeout
            )
            response.raise_for_status()
            data = response.json()
            self.token = data.get("access_token")
            
            if not self.token:
                raise Exception("Failed to get authentication token")
            
            # Set authorization header for all subsequent requests
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
            
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_data = response.json()
                error_detail = error_data.get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise Exception(f"Authentication error: {error_detail}")
        except Exception as e:
            raise Exception(f"Failed to authenticate: {str(e)}")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute HTTP request to API
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint
            data: Data to send in request body (for POST)
            params: Query parameters
            
        Returns:
            API response as dictionary
            
        Raises:
            Exception: On request error
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=None,  # No timeout
            )
            
            # For DELETE requests with 204 (No Content) return success
            if response.status_code == 204:
                return {"status": "success", "message": "Resource deleted"}
            
            # Check for specific errors before raise_for_status
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    detail = error_data.get("detail", "")
                    if "already enabled" in str(detail).lower():
                        print("⚠ Gateway already activated, continuing...")
                        return {"status": "success", "message": "Gateway already enabled"}
                except Exception:
                    pass
 
            
            # If response is empty, return success
            if not response.content:
                return {"status": "success"}
                
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            error_detail = "Unknown error"
            try:
                error_data = response.json()
                error_detail = error_data.get("detail", str(e))
            except Exception:
                error_detail = str(e)
            
            raise Exception(f"HTTP Error {response.status_code}: {error_detail}")
        except requests.exceptions.ConnectionError as e:
            raise Exception(
                f"Failed to connect to API at {url}\n"
                f"Check:\n"
                f"  1. Correct address (--base-url)\n"
                f"  2. Server availability\n"
                f"  3. API service is running\n"
                f"Error details: {str(e)}"
            )
        except requests.exceptions.Timeout as e:
            raise Exception(f"Response timeout from {url}: {str(e)}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

    def wait_for_task(self, task_id: str, timeout: int = None, check_interval: int = 2) -> bool:
        """
        Wait for task completion
        
        Args:
            task_id: Task ID
            timeout: Maximum wait time in seconds (None = no limit)
            check_interval: Check interval in seconds
            
        Returns:
            True if task completed successfully, False otherwise
        """
        start_time = time.time()
        
        while timeout is None or (time.time() - start_time < timeout):
            try:
                result = self._make_request("GET", f"/api/proxy/tasks/{task_id}")
                status = result.get("status")
                
                if status == "completed":
                    print(f"✓ Task {task_id} completed successfully")
                    return True
                elif status == "failed":
                    print(f"✗ Task {task_id} failed: {result.get('message')}")
                    return False
                else:
                    print(f"⏳ Task {task_id} status: {status}")
                    
            except Exception as e:
                print(f"⚠ Error checking task status: {e}")
            
            time.sleep(check_interval)
        
        if timeout is not None:
            print(f"✗ Task {task_id} timeout exceeded")
        return False

    def enable_gateway(
        self,
        node_id: Optional[str] = None,
        count: int = 1,
    ) -> Dict[str, Any]:
        """
        Enable iSCSI Gateway
        
        Args:
            node_id: Node ID for gateway activation
            count: Number of reactor threads
            
        Returns:
            Gateway information
        """
        print(f"\n{'='*60}")
        print("Step 1: Activating iSCSI Gateway")
        print(f"{'='*60}")
        
        params = {"count": count}
        if node_id:
            params["node_id"] = node_id
            
        try:
            result = self._make_request("POST", "/api/proxy/iscsi/gateways", params=params)
            
            # If result contains task_id, wait for completion
            if isinstance(result, dict) and "payload" in result and isinstance(result["payload"], dict):
                task_data = result["payload"]
                if "task_id" in task_data:
                    print(f"⏳ Task created: {task_data['task_id']}")
                    if self.wait_for_task(task_data["task_id"]):
                        # Get gateway list after activation
                        gateways = self._make_request("GET", "/api/proxy/iscsi/gateways")
                        if gateways.get("gateways"):
                            result = gateways["gateways"][0]
            
            gateway_node = result.get("node", node_id or "unknown")
            print(f"✓ Gateway activated on node: {gateway_node}")
            return result
            
        except Exception as e:
            print(f"✗ Gateway activation error: {e}")
            raise

    def create_portal(
        self,
        ip: str,
        port: int = 3260,
        tag: Optional[int] = None,
        name: Optional[str] = None,
        node_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create iSCSI Portal
        
        Args:
            ip: Portal IP address
            port: Port (default 3260)
            tag: Portal tag (optional)
            name: Portal name (optional)
            node_id: Node ID
            
        Returns:
            Portal information
        """
        print(f"\n{'='*60}")
        print("Step 2: Creating iSCSI Portal")
        print(f"{'='*60}")
        
        # If IP not specified or 0.0.0.0, use IP from base_url
        if ip == "0.0.0.0":
            # Extract IP from base_url
            try:
                host_part = self.base_url.split("://")[1].split(":")[0]
                ip = host_part
                print(f"  Using IP from base_url: {ip}")
            except Exception:
                print(f"  ⚠ Failed to extract IP from base_url, using {ip}")
        
        data = {
            "ip": ip,
            "port": port,
            "skip_etcd": False,
        }
        
        if tag is not None:
            data["tag"] = tag
        if name:
            data["name"] = name
        if node_id:
            data["node_id"] = node_id
            
        try:
            result = self._make_request("POST", "/api/proxy/iscsi/portals", data=data)
            
            # Extract tag from response if available
            extracted_tag = None
            if isinstance(result, dict) and "message" in result:
                # Parse message to get tag
                # Format: ["Portal 1 created on node1"]
                messages = result.get("message", [])
                if messages and len(messages) > 0:
                    msg = messages[0]
                    if "Portal" in msg:
                        parts = msg.split()
                        if len(parts) >= 2:
                            try:
                                extracted_tag = int(parts[1])
                                result["tag"] = extracted_tag
                            except ValueError:
                                pass
            
            # If we specified tag in request, use it
            if tag is not None and extracted_tag is None:
                result["tag"] = tag
                extracted_tag = tag
            
            print(f"✓ Portal created: {ip}:{port} (tag: {extracted_tag if extracted_tag else 'unknown'})")
            
            return result
            
        except Exception as e:
            print(f"✗ Portal creation error: {e}")
            raise

    def create_auth_group(
        self,
        tag: int,
        name: str,
        chap_str: str,
        skip_etcd: bool = False,
    ) -> Dict[str, Any]:
        """
        Create Authentication Group
        
        Args:
            tag: Auth group tag
            name: Auth group name
            chap_str: CHAP string (e.g., "user:admin secret:password123")
            skip_etcd: Skip saving to etcd
            
        Returns:
            Auth group information
        """
        print(f"\n{'='*60}")
        print("Step 3: Creating Authentication Group")
        print(f"{'='*60}")
        
        data = {
            "tag": tag,
            "name": name,
            "chap_str": chap_str,
            "skip_etcd": skip_etcd,
        }
        
        try:
            result = self._make_request("POST", "/api/proxy/iscsi/auth-groups", data=data)
            print(f"✓ Auth Group created: {name} (tag: {tag})")
            return result
            
        except Exception as e:
            error_str = str(e)
            # If auth group already exists, it's not critical
            if "already exists" in error_str.lower() or "409" in error_str:
                print(f"⚠ Auth Group with tag {tag} already exists, continuing...")
                return {"status": "success", "message": "Auth group already exists", "tag": tag}
            print(f"✗ Auth Group creation error: {e}")
            raise

    def get_portals(self) -> Dict[str, Any]:
        """
        Get list of all iSCSI portals
        
        Returns:
            List of portals
        """
        try:
            result = self._make_request("GET", "/api/proxy/iscsi/portals", params={})
            return result
        except Exception as e:
            print(f"⚠ Error getting portal list: {e}")
            return {"portals": []}

    def create_client(
        self,
        name: str,
        iqns: str,
        client_type: str = "single",
        netmasks: str = "ANY",
        tag: Optional[int] = None,
        auth_type: Optional[str] = None,
        auth_group_tag: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create iSCSI Client (Initiator Group)
        
        Args:
            name: Client/group name
            iqns: IQN string (or multiple separated by space)
            client_type: Client type (single or group)
            netmasks: Network masks (default ANY)
            tag: Client tag (optional)
            auth_type: Authentication type (none, oneway, mutual)
            auth_group_tag: Auth group tag for authentication
            
        Returns:
            Client information
        """
        print(f"\n{'='*60}")
        print("Step 4: Creating iSCSI Client (Initiator Group)")
        print(f"{'='*60}")
        
        data = {
            "type": client_type,
            "name": name,
            "iqns": iqns,
            "netmasks": netmasks,
        }
        
        if tag is not None:
            data["tag"] = tag
        if auth_type is not None:
            data["auth_type"] = auth_type
        if auth_group_tag is not None:
            data["auth_group_tag"] = auth_group_tag
            
        try:
            result = self._make_request("POST", "/api/proxy/iscsi/clients", data=data)
            print(f"✓ Client created: {name} (IQN: {iqns})")
            return result
            
        except Exception as e:
            print(f"✗ Client creation error: {e}")
            raise

    def get_pools(self) -> Dict[str, Any]:
        """
        Get list of all pools
        
        Returns:
            List of pools
        """
        try:
            result = self._make_request("GET", "/api/proxy/pools", params={})
            return result
        except Exception as e:
            print(f"⚠ Error getting pool list: {e}")
            return {"payload": []}

    def create_pool(
        self,
        name: str,
        pool_type: str = "replicated",
        pg_size: int = 2,
        pg_count: Optional[int] = None,
        parity_chunks: Optional[int] = None,
        force: bool = False,
    ) -> Dict[str, Any]:
        """
        Create Pool
        
        Args:
            name: Pool name
            pool_type: Pool type (replicated or ec)
            pg_size: PG size
            pg_count: Number of PGs (optional)
            parity_chunks: Number of parity chunks for EC pools
            force: Force creation
            
        Returns:
            Pool information
        """
        print(f"\n{'='*60}")
        print("Step 5: Creating Pool")
        print(f"{'='*60}")
        
        params = {
            "name": name,
            "pg_size": pg_size,
            "force": force,
        }
        
        if pg_count is not None:
            params["pg_count"] = pg_count
        if parity_chunks is not None:
            params["parity_chunks"] = parity_chunks
            
        try:
            result = self._make_request("POST", f"/api/proxy/pools/{pool_type}", params=params)
            
            # Wait for task completion if exists
            if isinstance(result, dict) and "payload" in result:
                task_data = result.get("payload", {})
                if isinstance(task_data, dict) and "task_id" in task_data:
                    print(f"⏳ Task created: {task_data['task_id']}")
                    if self.wait_for_task(task_data["task_id"]):
                        # Verify that pool was actually created
                        print(f"  Checking pool existence...")
                        pools_result = self.get_pools()
                        
                        pool_found = False
                        if isinstance(pools_result, dict) and "payload" in pools_result:
                            pools = pools_result.get("payload", [])
                            for pool in pools:
                                if isinstance(pool, dict) and pool.get("name") == name:
                                    pool_found = True
                                    print(f"  ✓ Pool '{name}' found in pool list")
                                    break
                        
                        if not pool_found:
                            print(f"  ⚠ Pool '{name}' not found in list, but may still be creating")
            
            print(f"✓ Pool created: {name} (type: {pool_type}, pg_size: {pg_size})")
            return result
            
        except Exception as e:
            print(f"✗ Pool creation error: {e}")
            raise

    def get_images(self, details: bool = True) -> Dict[str, Any]:
        """
        Get list of all images
        
        Args:
            details: Get detailed information
            
        Returns:
            List of images
        """
        try:
            result = self._make_request("GET", "/api/proxy/images", params={"details": details})
            return result
        except Exception as e:
            print(f"⚠ Error getting image list: {e}")
            return {"payload": []}

    def create_image(
        self,
        name: str,
        pool: str,
        size: str,
        greater_size: bool = False,
    ) -> Dict[str, Any]:
        """
        Create Image
        
        Args:
            name: Image name
            pool: Pool name
            size: Size (e.g., "10G", "1024M")
            greater_size: Allow size greater than pool size
            
        Returns:
            Image information
        """
        print(f"\n{'='*60}")
        print("Step 6: Creating Image")
        print(f"{'='*60}")
        
        params = {
            "name": name,
            "pool": pool,
            "size": size,
            "greater_size": greater_size,
        }
        
        try:
            result = self._make_request("POST", "/api/proxy/images", params=params)
            
            # Wait for task completion
            if isinstance(result, dict) and "payload" in result:
                task_data = result.get("payload", {})
                if isinstance(task_data, dict) and "task_id" in task_data:
                    print(f"⏳ Task created: {task_data['task_id']}")
                    if self.wait_for_task(task_data["task_id"]):
                        # Verify that image was actually created
                        print(f"  Checking image existence...")
                        images_result = self.get_images(details=True)
                        
                        image_found = False
                        if isinstance(images_result, dict) and "payload" in images_result:
                            images = images_result.get("payload", [])
                            for image in images:
                                if isinstance(image, dict) and image.get("name") == name:
                                    image_found = True
                                    image_size_actual = image.get("size", "unknown")
                                    image_pool = image.get("pool", "unknown")
                                    print(f"  ✓ Image '{name}' found in image list")
                                    print(f"    Pool: {image_pool}, Size: {image_size_actual} bytes")
                                    break
                        
                        if not image_found:
                            print(f"  ⚠ Image '{name}' not found in list, but may still be creating")
            
            print(f"✓ Image created: {name} in pool {pool} size {size}")
            return result
            
        except Exception as e:
            print(f"✗ Image creation error: {e}")
            raise

    def export_iscsi(
        self,
        gateway: str,
        portal_id: int,
        host_id: str,
        lun_id: int,
        image_name: str,
        force: bool = False,
        block_size: int = 512,
        node_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Export image via iSCSI
        
        Args:
            gateway: ID gateway
            portal_id: Portal ID
            host_id: Host ID (client name)
            lun_id: LUN ID
            image_name: Image name (pool/image)
            force: Force export
            block_size: Block size
            node_id: Node ID
            
        Returns:
            Export information
        """
        print(f"\n{'='*60}")
        print("Step 7: Exporting image via iSCSI")
        print(f"{'='*60}")
        
        data = {
            "gateway": gateway,
            "portal_id": portal_id,
            "host_id": host_id,
            "lun_id": lun_id,
            "image_name": image_name,
            "force": force,
            "block_size": block_size,
        }
        
        params = {}
        if node_id:
            params["node_id"] = node_id
            
        try:
            result = self._make_request("POST", "/api/proxy/iscsi/exports", data=data, params=params)
            print(f"✓ Image {image_name} exported via iSCSI")
            
            # Display export details
            if isinstance(result, dict):
                details = result.get("details", {})
                if isinstance(details, dict):
                    target_iqn = details.get("target_iqn")
                    if target_iqn:
                        print(f"  Target IQN: {target_iqn}")
                    print(f"  LUN ID: {lun_id}")
            
            return result
            
        except Exception as e:
            print(f"✗ iSCSI export error: {e}")
            raise

    def full_setup(
        self,
        # Gateway parameters
        gateway_node: Optional[str] = None,
        gateway_threads: int = 1,
        # Portal parameters
        portal_ip: str = "180.191.100.110",
        portal_port: int = 3260,
        portal_tag: Optional[int] = None,
        portal_name: Optional[str] = None,
        # Auth Group parameters
        auth_group_tag: int = 10,
        auth_group_name: str = "default_auth",
        auth_chap_str: str = "user:admin secret:Passw0rd",
        # Client parameters
        client_name: str = "testClient",
        client_iqn: str = "iqn.2024-01.com.example:initiator01",
        client_type: str = "single",
        client_tag: Optional[int] = None,
        client_auth_type: str = "oneway",
        # Pool parameters
        pool_name: str = "testPool",
        pool_type: str = "replicated",
        pg_size: int = 2,
        pg_count: Optional[int] = None,
        # Image parameters
        image_name: str = "testImage",
        image_size: str = "10M",
        # Export parameters
        lun_id: int = 0,
        block_size: int = 512,
        force: bool = False,
    ) -> Dict[str, Any]:
        """
        Perform full iSCSI setup from scratch
        
        Returns:
            Dictionary with information about all created entities
        """
        print(f"\n{'#'*60}")
        print("STARTING FULL iSCSI SETUP")
        print(f"{'#'*60}")
        print(f"✓ Authentication successful (user: {self.username})")
        print()
        
        results = {}
        
        try:
            # 1. Activate Gateway
            self.enable_gateway(node_id=gateway_node, count=gateway_threads)
            #TODO FIX RESPONSE HANDLING    
            # 2. Create Portal
            portal = self.create_portal(
                ip=portal_ip,
                port=portal_port,
                tag=portal_tag if portal_tag else 1,
                name=portal_name if portal_name else "defaultPortal",
                node_id=gateway_node if gateway_node else None,
            )
            results["portal"] = portal
            
            # Get portal_id from response
            portal_id_value = None
            if isinstance(portal, dict) and "tag" in portal:
                portal_id_value = portal["tag"]
            
            # Fallback to provided tag or default
            if portal_id_value is None:
                portal_id_value = portal_tag if portal_tag else 1
            
            print(f"  Using portal_id for export: {portal_id_value}")
            
            # Verify that portal was actually created
            print(f"\n📋 Verifying portal creation...")
            portals_response = self.get_portals()
            portals_list = portals_response.get("portals", [])
            
            portal_found = False
            for p in portals_list:
                if p.get("tag") == portal_id_value:
                    portal_found = True
                    print(f"✓ Portal verified: tag={portal_id_value}, ip={portal_ip}:{portal_port}")
                    break
            
            if not portal_found:
                print(f"⚠ Portal with tag {portal_id_value} not found in portal list")
                print(f"  Available portals: {[p.get('tag') for p in portals_list]}")
            else:
                print(f"  Total portals in system: {len(portals_list)}")
            
            # 3. Create Auth Group
            auth_group = self.create_auth_group(
                tag=auth_group_tag,
                name=auth_group_name,
                chap_str=auth_chap_str,
            )
            results["auth_group"] = auth_group
            
            # 4. Create Client
            client = self.create_client(
                name=client_name,
                iqns=client_iqn,
                client_type=client_type,
                tag=client_tag if client_tag else 1,
                auth_type=client_auth_type,
                auth_group_tag=auth_group_tag,
            )
            results["client"] = client
            
            # 5. Create Pool
            pool = self.create_pool(
                name=pool_name,
                pool_type=pool_type,
                pg_size=pg_size,
                pg_count=pg_count,
                force=force,
            )
            results["pool"] = pool
            
            # 6. Create Image
            image = self.create_image(
                name=image_name,  # Only image name, pool is passed separately
                pool=pool_name,
                size=image_size,
            )
            results["image"] = image
            
            # 7. Export via iSCSI
            # Get gateway_id for export
            gateway_id = gateway_node if gateway_node else self.base_url.split("://")[1].split(":")[0]
            
            # NOTE: Export uses ONLY image name without pool prefix
            # The image is stored in the system as just "testImage", not "testPool/testImage"
            print(f"\n📋 Preparing export...")
            print(f"  Image name: {image_name}")
            print(f"  Pool: {pool_name}")
            
            export = self.export_iscsi(
                gateway=gateway_id,
                portal_id=portal_id_value,  # Use actual portal tag
                host_id=client_name,
                lun_id=lun_id,
                image_name=image_name,  # Only image name, WITHOUT pool prefix
                force=force,
                block_size=block_size,
                node_id=gateway_node,  # Use gateway_node (может быть None)
            )
            results["export"] = export
            
            print(f"\n{'#'*60}")
            print("✓ FULL iSCSI SETUP COMPLETED SUCCESSFULLY!")
            print(f"{'#'*60}\n")
            
            # Display summary
            print("SUMMARY OF CREATED ENTITIES:")
            print(f"  Gateway: {gateway_id}")
            print(f"  Portal: {portal_ip}:{portal_port} (tag: {portal_id_value})")
            print(f"  Auth Group: {auth_group_name} (tag: {auth_group_tag})")
            print(f"  Client: {client_name} (IQN: {client_iqn}, auth: {client_auth_type})")
            print(f"  Pool: {pool_name} (type: {pool_type})")
            print(f"  Image: {image_name} in pool {pool_name} (size: {image_size})")
            
            # Display connection information
            if isinstance(export, dict) and "details" in export:
                details = export.get("details", {})
                if isinstance(details, dict):
                    target_iqn = details.get("target_iqn")
                    if target_iqn:
                        print(f"\n{'='*60}")
                        print("CONNECTION INFORMATION:")
                        print(f"{'='*60}")
                        print(f"  Target IQN: {target_iqn}")
                        print(f"  Portal: {portal_ip}:{portal_port}")
                        print(f"  LUN: {lun_id}")
                        print(f"\nDiscovery command (Linux):")
                        print(f"  iscsiadm -m discovery -t st -p {portal_ip}:{portal_port}")
                        print(f"\nConnection command (Linux):")
                        print(f"  iscsiadm -m node -T {target_iqn} -p {portal_ip}:{portal_port} --login")
            
            return results
            
        except Exception as e:
            print(f"\n{'#'*60}")
            print(f"✗ ERROR DURING SETUP: {e}")
            print(f"{'#'*60}\n")
            raise


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Script for creating complete iSCSI configuration from scratch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:

  # Basic setup with default parameters
  python create_iscsi_setup.py --base-url http://localhost:8000

  # Full setup with custom parameters
  python create_iscsi_setup.py \\
    --base-url http://localhost:8000 \\
    --username admin \\
    --password MyCustomPassword \\
    --portal-ip 192.168.1.100 \\
    --client-iqn iqn.2024-01.com.mycompany:server01 \\
    --pool-name mypool \\
    --image-name myimage \\
    --image-size 50G

  # Output results in JSON
  python create_iscsi_setup.py --base-url http://localhost:8000 --json
        """,
    )
    
    # Main parameters
    parser.add_argument(
        "--base-url",
        required=True,
        help="Base API URL (e.g., http://localhost:8000)",
    )
    parser.add_argument("--username", default="admin", help="Username (default: admin)")
    parser.add_argument("--password", default="Passw0rd", help="Password (default: Passw0rd)")
    parser.add_argument("--no-verify-ssl", action="store_true", help="Do not verify SSL certificate")
    
    # Gateway parameters
    parser.add_argument("--gateway-node", help="Node ID for gateway (optional)")
    parser.add_argument("--gateway-threads", type=int, default=1, help="Number of gateway threads (default: 1)")
    
    # Portal parameters
    parser.add_argument("--portal-ip", default="0.0.0.0", help="Portal IP address (default: 0.0.0.0)")
    parser.add_argument("--portal-port", type=int, default=3260, help="Portal port (default: 3260)")
    parser.add_argument("--portal-tag", type=int, help="Portal tag (optional)")
    parser.add_argument("--portal-name", help="Portal name (optional)")
    
    # Auth Group parameters
    parser.add_argument("--auth-group-tag", type=int, default=10, help="Auth group tag (default: 10)")
    parser.add_argument("--auth-group-name", default="default_auth", help="Auth group name (default: default_auth)")
    parser.add_argument("--auth-chap-str", default="user:admin secret:Passw0rd", help="CHAP string (default: user:admin secret:Passw0rd)")
    
    # Client parameters
    parser.add_argument("--client-name", default="testClient", help="Client name (default: test_client)")
    parser.add_argument(
        "--client-iqn",
        default="iqn.2024-01.com.example:initiator01",
        help="Client IQN (default: iqn.2024-01.com.example:initiator01)",
    )
    parser.add_argument("--client-type", choices=["single", "group"], default="single", help="Client type")
    parser.add_argument("--client-tag", type=int, help="Client tag (optional)")
    parser.add_argument("--client-auth-type", choices=["none", "oneway", "mutual"], default="oneway", help="Client authentication type")
    
    # Pool parameters
    parser.add_argument("--pool-name", default="testPool", help="Pool name (default: test_pool)")
    parser.add_argument("--pool-type", choices=["replicated", "ec"], default="replicated", help="Pool type")
    parser.add_argument("--pg-size", type=int, default=2, help="PG size (default: 2)")
    parser.add_argument("--pg-count", type=int, help="Number of PGs (optional)")
    
    # Image parameters
    parser.add_argument("--image-name", default="testImage", help="Image name (default: test_image)")
    parser.add_argument("--image-size", default="10M", help="Image size (default: 10G)")
    
    # Export parameters
    parser.add_argument("--lun-id", type=int, default=0, help="LUN ID (default: 0)")
    parser.add_argument("--block-size", type=int, default=512, help="Block size (default: 512)")
    parser.add_argument("--force", action="store_true", help="Force creation/export")
    
    # Output
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    args = parser.parse_args()
    
    try:
        # Creating manager
        manager = ISCSISetupManager(
            base_url=args.base_url,
            username=args.username,
            password=args.password,
            verify_ssl=not args.no_verify_ssl,
        )
        
        # Performing full setup
        results = manager.full_setup(
            gateway_node=args.gateway_node,
            gateway_threads=args.gateway_threads,
            portal_ip=args.portal_ip,
            portal_port=args.portal_port,
            portal_tag=args.portal_tag,
            portal_name=args.portal_name,
            auth_group_tag=args.auth_group_tag,
            auth_group_name=args.auth_group_name,
            auth_chap_str=args.auth_chap_str,
            client_name=args.client_name,
            client_iqn=args.client_iqn,
            client_type=args.client_type,
            client_tag=args.client_tag,
            client_auth_type=args.client_auth_type,
            pool_name=args.pool_name,
            pool_type=args.pool_type,
            pg_size=args.pg_size,
            pg_count=args.pg_count,
            image_name=args.image_name,
            image_size=args.image_size,
            lun_id=args.lun_id,
            block_size=args.block_size,
            force=args.force,
        )
        
        # Outputting results
        if args.json:
            print("\n" + json.dumps(results, indent=2, ensure_ascii=False))
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n✗ Critical error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())


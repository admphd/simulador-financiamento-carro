
# Simulador de Financimento de Veículos
Este simulador foi construido com a intenção de fazer o levantamento de custos para a compra de um veículo novo.

Porém, durante a construção, percebi que poderia fazer algo mais robusto e iniciei a incrementar funções.

Até o momento o simulador faz o cálculo aproximado do valor da parcela de um financiamento com base na taxa de juros de cada banco disponibilizado pelo site do Banco Central.

O simulador também calcula o valor aproximado do IPVA (atualmente, a base de cálculo é a taxa de IPVA do estado de Goiás. Pretendo implementar a opção de escolher o estado e o simulador realizar o cálculo com base na taxa do estado escolhido), calcula um valor aproximado de seguro (aqui é um terreno obscuro, pois o valor do seguro utiliza N varáveis para chegar a uma cotação. Aqui estou usando um "taxa" fixa de 5,5% do valor  aproximado de mercado do veículo).

Este simulador ainda está em construção, portanto erros podem ocorrer, e novas funcionalidades podem ser adicionados ao longo do tempo.

Fique a vontade para sugerir melhorias.


## Screenshots

![App Screenshot](https://z-p3-scontent.fgyn18-1.fna.fbcdn.net/v/t39.30808-6/718687826_27652589707660866_3292094499476275544_n.jpg?stp=dst-jpg_tt6&cstp=mx1095x667&ctp=s1095x667&_nc_cat=106&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeF13Twh0P2B7k3wKGjIizQMF3F88qXpMqgXcXzypekyqGdycpJVMC3PDXq3IwVp3KW4P7w3zoYRaF0yBs5iX13g&_nc_ohc=CeCA_1CzX14Q7kNvwHOc528&_nc_oc=AdpL7ZJ968LtWTJsDDEN4naQKIXCyQb8YJqWTCAvZaDyh61LBbkwuZEnoXAGV-aEqhM&_nc_zt=23&_nc_ht=z-p3-scontent.fgyn18-1.fna&_nc_gid=jeL2wf-PmYCm9goEiegbjA&_nc_ss=7b2a8&oh=00_Af9wDfw3jIyM8KWAWLVRvZs9GW2hwDIDrZ-FiAFkHyAZ6A&oe=6A29E3A9)

![App Screenshot](https://z-p3-scontent.fgyn18-1.fna.fbcdn.net/v/t39.30808-6/718033231_27652589634327540_4935850250724243716_n.jpg?stp=dst-jpg_tt6&cstp=mx1061x996&ctp=s1061x996&_nc_cat=109&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeGGKTfUOuxuK10ZBq9nAGTaJePS8g3RTOMl49LyDdFM46fUnR7q519V8_nW5Fn6W1NhyPwDObQKCzRv4JQRZVV0&_nc_ohc=KsMbxMinCXwQ7kNvwF2DohE&_nc_oc=AdqErKvHeUn6QsSgpD--7suXul5eaaWPjevxAN0Ii7WpjLXVirMjmtRXWF34kZ5wNEU&_nc_zt=23&_nc_ht=z-p3-scontent.fgyn18-1.fna&_nc_gid=Eoi0oL0zdbOBLaqqOr845A&_nc_ss=7b2a8&oh=00_Af_LBdUOKF9FWSnHK_MnTHPwEGaoLSXRMWixW9gu0jPPFg&oe=6A29E185)

![App Screenshot](https://z-p3-scontent.fgyn18-1.fna.fbcdn.net/v/t39.30808-6/715651479_27652589264327577_828320590951623000_n.jpg?stp=dst-jpg_tt6&cstp=mx1045x507&ctp=s1045x507&_nc_cat=102&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeFscz4oJXfXeuC9eDzu0ukCb2r26nkC32tvavbqeQLfa9OLm9z0sjuFH8el5kKvmjgyR7gLuX3lsdE8XoPznOLr&_nc_ohc=RZmqVCpWs-UQ7kNvwFlSI80&_nc_oc=AdoLgt-SgsnFQZ14LlS3HJV0lHFcVQDo14nokwlFb0Xo3wKb81l9wlAI0TS5ahcj-5w&_nc_zt=23&_nc_ht=z-p3-scontent.fgyn18-1.fna&_nc_gid=lUYPdyCULTGr5_ZUrnVmXw&_nc_ss=7b2a8&oh=00_Af-FHx70G3kOrLQ_vZFIxlxcl2oTtECoO3y0JKN6wxc4pg&oe=6A29FE92)

![App Screenshot](https://z-p3-scontent.fgyn18-1.fna.fbcdn.net/v/t39.30808-6/717341112_27652589294327574_8541904586315347056_n.jpg?stp=dst-jpg_tt6&cstp=mx1002x465&ctp=s1002x465&_nc_cat=105&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeH_lvzicF_pm-zxP0smcQaupBgSMdXexj6kGBIx1d7GPhN1W5KKKGRsxqQ-G2M2gDEGguDjynH8kIG38vLdgXfz&_nc_ohc=C1SqiVtGZX0Q7kNvwHOEBXY&_nc_oc=Adomq2qI1m7EruQ6aDAcJBvI-u4HBfTOaw0_htAU6PCGzGx8ViWgZngQDoUjY2veQ_M&_nc_zt=23&_nc_ht=z-p3-scontent.fgyn18-1.fna&_nc_gid=HQlq3Gy5QA4Zee9RnTsgFw&_nc_ss=7b2a8&oh=00_Af9xSOTonN_vOI6pX11uf9bqwrIgM5bQ-iTOEDE5r2dV7A&oe=6A29EEDB)

![App Screenshot](https://z-p3-scontent.fgyn18-1.fna.fbcdn.net/v/t39.30808-6/716922536_27652589354327568_5823272126143453093_n.jpg?stp=dst-jpg_tt6&cstp=mx1083x1447&ctp=s1083x1447&_nc_cat=106&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeHvp-tPv8wnDzNOo-mY0pJKpeYGaM-FGvGl5gZoz4Ua8bmu8U66DlBIr-NJU0N5LoVgd8HY6MFhovibZD7adgtG&_nc_ohc=sQs_nFHw7MsQ7kNvwEB0C_X&_nc_oc=AdpKNMW5ojX5pMFgFX8nvPahfwSTxGW2k0GgAcTDryhM8bk5v-kd04QjsNb4LykiHo0&_nc_zt=23&_nc_ht=z-p3-scontent.fgyn18-1.fna&_nc_gid=1J5VG0T5iM0gH5DSH_tgnw&_nc_ss=7b2a8&oh=00_Af-7JR8FUJlEqkjnmocHjR9uxCPYcfw73m6xB-IsTI_osw&oe=6A2A0A94)

![App Screenshot](https://z-p3-scontent.fgyn18-1.fna.fbcdn.net/v/t39.30808-6/717249648_27652589727660864_6019561365511277330_n.jpg?stp=dst-jpg_tt6&cstp=mx993x1881&ctp=s993x1881&_nc_cat=108&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeHWujbptraK7hG6zG251oxpqWzuaHu1rRSpbO5oe7WtFPN7tFYb1GWTeJbX5RzM5rI7-5sfoiSwcGyiBoNUMWgR&_nc_ohc=FxNSJD_RxkYQ7kNvwF4kMgg&_nc_oc=AdpNNq6GGcWbUJTjWXaCE-BKjOIuVuXEduq34tRBq6ofk2vm6WvOldPBbeyAn0Zqdx0&_nc_zt=23&_nc_ht=z-p3-scontent.fgyn18-1.fna&_nc_gid=rHQ2L0D1W8l6qMIg8lj7WA&_nc_ss=7b2a8&oh=00_Af-vBkRkiR1xNHEjOiyRIEb2TiBp0uxHTLXZ_bUZ7Y0QeA&oe=6A29E8AE)



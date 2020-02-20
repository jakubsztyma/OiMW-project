# Using Extractor

### Python Setup
User should:

* have python with version 3.6, 
* installed *pipenv* python package, 
* use console other than PowerShell.


In folder with *main.py* run:
```bash
pipenv install
pipenv shell
```

### UCI client configuration

File *uci_server_config.json* contains configuration of UCI client. 
It can be changed to facilitate connecting to remote UCI server.

Example configuration file:
```json
{
  "login": "test",
  "password": "111111",
  "uci_server_url": "http://localhost:8080/",
  "uci_server_socket_url": "ws://localhost:8080/ws_engine"
}
```

### How to run program (example)

```bash
python ./main.py -h minimal  -cp 20 -depth 10 -alt 3 -cpu_cores 2 -input_path test_pgn.pgn  -output_path out.test
```


# Opis filtrów (filter description)

Brief description in English is available in *filters.py* file.

### *not_only_move*

Zadaniem tego filtru jest wykluczenie takich ruchów, które nie mają alternatyw.
Ze względu na to, że w danym położeniu jest to jedyny legalny ruch, to nie jest on dla nas ciekawy. 


### *not_losing*

Sprawdzenie czy ruch prowadzi do przegranej. 
Jeżeli najlepszy ruch dla zadanej głębokości prowadzi do przegranej, to jego analiza jest zbędna. 
Nie ma możliwości wygranej w takim położeniu w czasu gry, jeżeli gracz przeciwny nie popełni błędu.


### *not_a_starting_move*

Pierwsze kilka ruchów jest pomijanych. 
Jakkolwiek pewne otwarcia można uznać za lepsze od innych, to ich znalezienie przy użyciu tego programu nie będzie pożyteczny.
Wiedza na ich temat byłaby dostać płytka, w porównaniu do informacji o nich dostępnych z innych źródeł.

Jest możliwe dostosowywanie filtru za pomocą parametru *n_ignore* dającego możliwość wyboru, ile pierwszych ruchów ma być ignorowanych.


### *better_than_second*

Filtra ma za zadanie sprawdzić o ile lepszy jest ruch najlepszy of drugiego najlepszego ruchu dla zadanej głębokości. 
Jeżeli istnieje wiele ruchów z tej samej pozycji o podobnej jakości (wartość *cp*) to ten ruch prawdopodobnie nie jest warty analizy, bo są dla niego dostępne niedużo gorsze alternatywy.

Jest możliwe dostosowywanie filtru za pomocą parametru *min_diff* dającego możliwość wyboru różnicy w *cp* od której najlepszy ruch można uznać za wystarczająco lepszy od kolejnego.



### *not_strong_in_given_depth*

Sprawdza czy najlepszy ruch był również najlepszy na innej, zadanej, głębokości.
Przykładowo możliwe jest sprawdzenie czy ruch najlepszy dla głębokości 20 był również najlepszy dla głębokości 5.

Ruch, który jest najlepszy dla jednocześnie niskich i wysokich głębokości może być uznany za oczywisty i nie warty analizy. 
I takie przypadki mają być odrzucane przez filtr.
Ruchy które są najlepsze tylko dla dużych głębokości mogą być trudne do wywnioskowania przez człowieka, ze względu na konieczność patrzenia na bardzo dużo kroków do przodu.
Z tego powodu warto je analizować i wypracować intuicję ich dotyczącą.

Jest możliwe dostosowywanie filtru za pomocą parametru *depth* dającego możliwość wyboru głębokości, na której ma zostać dokonane sprawdzenie.


### *not_check*

Sprawdzenie czy ruch nie prowadzi do szachu. 
Końcowe zagrania są mało interesujące do analizy. 
Lepsze do tego zadania są Endgame tablebase.


### *is_not_best_material_gain*

Filtr ma za zadanie sprawdzić, czy w przypadku, jeżeli najlepszy ruch prowadzi do zdobycia przewagi w materiale, to czy lepsze wymiany (w perspektywie pojedynczego ruchu) są dostępne.
Zagrania prowadzące do zdobycia najlepszej figury przeciwnika są oczywiste dla człowieka. W większości przypadków są rozważane przez niego w pierwszej kolejności.
Dlatego w sytuacji, kiedy najlepszym ruchem dla zadanej głębokości jest zdobycie figury o mniejszej wartości, pomimo dostępu do zdobycia figur lepszych, warto przeanalizować takie położenie.

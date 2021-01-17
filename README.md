# sales-store
1. Authentification Service:

    - pt login username:cristina parola:cristina
    - [x] login 
    - [x] logout 
    - [ ] register 
    - [x] validateCredentials 
    
2. StockService
    
    - [x] getStock  
    - [x] getStockById 
    - [x] getStockByName 
    - [x] updateStock 
    - [ ] sendStock ?
    - [ ] processStock ?
    
3. OrderService

    -tab nou Order in care facem comenzi (refolosim Add purchase)

    - [ ] placeOrder
    - [ ] proccessOrder
    - [ ] updateOrder
    
4. ReportService
    
    - [ ] getReportByTimeRange
    - [ ] getCustomReport
    - [ ] getCustomerReport
    - [ ] getStockReport
    - [ ] getOrderReport
    - [ ] sendReport
    
5. CustomerRequestService
    
    - [ ] sendCustomerRequest
    - [ ] porcessCustomerRequest
    
6. RecommendationService

    - [ ] getCustomerRemmendation
    - [ ] getRecommendation
    - [ ] sentRecommendation
    - [ ] processRecommendation

To deploy on localhost please run:

```bash
./script.sh # this will build the images
docker-compose up --build # to start the containers
docker-compose down # might consider using this
```

in browser -> http://localhost:3003/
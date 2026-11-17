# Chọn hình thức cho số liệu

Thứ tự đúng: **việc người đọc phải làm → hình thức → màu.** Phần lớn biểu đồ tệ bắt đầu bằng việc chọn màu. Tóm tắt từ nguyên tắc của skill `dataviz` đi kèm Claude Code; harness nào có skill đó thì đọc thêm bản đầy đủ và chạy script kiểm tra bảng màu của nó.

## Có cần biểu đồ không?
| Dữ liệu là | Dùng | Đừng dùng |
|---|---|---|
| Một giá trị hiện tại (có thể kèm xu hướng) | Stat tile: số + chênh lệch + sparkline | Biểu đồ cột có đúng một cột |
| Vài con số đầu bảng | Hàng KPI gồm các stat tile | Biểu đồ cột nhóm |
| Con số mà cả dashboard mở đầu bằng nó | Hero number: chữ sans cỡ lớn | Font serif hay font trang trí |
| Một tỷ lệ so với giới hạn | Thanh đo (meter) | Pie 2 lát |
| Hơn khoảng 7 nhóm đều có ý nghĩa | Bảng, hoặc bảng kèm biểu đồ | Thêm màu |

## Việc → loại biểu đồ
| Người đọc phải | Mặc định | Màu làm việc gì |
|---|---|---|
| So độ lớn | Cột hoặc thanh ngang (sắp xếp); heatmap cho dạng lưới | Tuần tự: một sắc độ, càng nhiều càng đậm |
| Xem xu hướng theo thời gian | Đường; vùng nếu chỉ có một chuỗi | Tuần tự, hoặc một màu định danh |
| Phân biệt các chuỗi | Cột nhóm hoặc chồng, nhiều đường | Định danh (categorical) |
| Thấy một chuỗi nổi bật giữa các chuỗi khác | **Nhấn mạnh**: một chuỗi có màu, còn lại xám | Một màu + xám |
| Thấy trên hay dưới mốc, chênh với mục tiêu | Thanh phân kỳ, hoặc đường có đường mốc | Phân cực: hai màu + giữa xám trung tính |
| Thấy một phần so với tổng thể | Thanh ngang xếp hạng (so các phần); thanh phân đoạn ≤ 6 phần (nhìn nhanh); cột chồng (thay đổi theo thời gian) | Định danh |
| Đọc thang thứ bậc (Likert, hài lòng) | Thanh chồng phân kỳ, lấy mức trung tính làm tâm | Phân cực |
| So trước/sau từng mục | Dumbbell | Một màu, hai sắc độ |
| Xem phân bố | Histogram, box plot, strip plot | Một màu |
| Xem quan hệ hai biến | Scatter (thêm đường xu hướng nếu có ý nghĩa) | Một màu; tối đa 3 nhóm |
| Xem phễu | Thanh ngang giảm dần, ghi tỷ lệ rơi giữa các bước | Một màu |
| Xem cohort / retention | Heatmap tam giác | Tuần tự |
| Xem theo địa lý | Bản đồ choropleth đã chuẩn hóa theo dân số hoặc diện tích | Tuần tự |

## Quy tắc không thương lượng
- **Một trục y.** Hai thang đo khác nhau thì dùng hai biểu đồ, small multiples, hoặc quy về chỉ số chung (index = 100).
- **Màu định danh đi theo thực thể, gán theo thứ tự cố định.** Lọc bớt chuỗi thì các chuỗi còn lại không được đổi màu. Không tự sinh màu thứ 9: gộp vào "Khác", hoặc tách thành small multiples.
- **Tuần tự là một sắc độ, nhạt tới đậm.** Không dùng cầu vồng.
- **Phân kỳ là hai màu ở hai cực, giữa là xám trung tính.**
- **Màu trạng thái** (tốt, cảnh báo, nghiêm trọng, nguy cấp) để dành riêng, và luôn đi kèm icon hoặc chữ, không bao giờ chỉ dùng màu.
- **Chữ dùng màu chữ**, không dùng màu của chuỗi. Nhãn, giá trị và chú giải ở màu chữ chính hoặc phụ; ô màu bên cạnh làm nhiệm vụ định danh.
- **Từ 2 chuỗi trở lên phải có chú giải**; ≤ 4 chuỗi thì ghi nhãn trực tiếp lên đường hoặc thanh. Một chuỗi thì không cần chú giải, tiêu đề đã nói nó là gì.
- **Nét mảnh, lưới nhạt, không viền quanh các mark**; giữa các khối liền nhau để một khe nhỏ cùng màu nền. Không ghi số lên mọi điểm.
- **Người mù màu**: kiểm bằng công cụ, không kiểm bằng mắt. Các cặp màu kề nhau phải phân biệt được cả khi mô phỏng mù màu đỏ–lục.
- **Trục cột bắt đầu từ 0.** Trục đường được phép không bắt đầu từ 0, nhưng phải ghi rõ.

## Dấu hiệu sai
Biểu đồ hai trục y · pie hoặc donut để so các giá trị sát nhau · 3D cho biểu đồ 2D · đổi màu khi lọc · tooltip là cách duy nhất để đọc số · bộ lọc nằm trong từng card · nhãn bị cắt hoặc tràn khỏi thanh · lưới nét đứt · số trên mọi điểm · cầu vồng cho độ lớn · màu trạng thái dùng cho chuỗi thường.

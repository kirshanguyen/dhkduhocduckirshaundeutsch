# Website Tiếng Đức DHK — Góc chia sẻ

Website gốc + chuyên mục Góc chia sẻ. Chỉ chủ repository có quyền tạo và sửa bài.

## Đăng bài trực tiếp bằng GitHub (không cần tải ZIP)

1. Vào repository trên GitHub, mở thư mục `posts`.
2. Chọn **Add file → Create new file**. Đặt tên dạng `ten-bai-viet.md` (không dấu, dấu gạch nối).
3. Sao chép cấu trúc trong `posts/_MAU_BAI_VIET.md`. Đổi `title`, `date` (YYYY-MM-DD), `category`, `description`, nội dung.
4. `category` phải đúng một trong: `Học tiếng Đức`, `Du học đại học Đức`, `Du học nghề Đức`, `Cuộc sống tại Đức`.
5. Nếu muốn ảnh bìa, tải ảnh vào `assets/` và ghi `image: assets/ten-anh.jpg`. Nếu không, xóa dòng `image`.
6. Chọn **Commit changes**. Cloudflare Pages tự cập nhật sau khi repository đã kết nối Git.
7. Muốn sửa bài: mở file `.md` → biểu tượng bút chì → sửa → Commit changes.

Lưu ý: `_MAU_BAI_VIET.md` không được xuất bản. Không đăng thông tin riêng tư hay tài liệu độc quyền lên repository Public.

## Cloudflare Pages Git integration

- Framework preset: **None**
- Production branch: **main**
- Build command: `python3 scripts/build.py`
- Build output directory: `dist`
- Root directory: `/`

Cloudflare Pages dự án Direct Upload cũ không chuyển trực tiếp sang Git integration. Hãy tạo **dự án Pages mới**, thử trên URL mới rồi chuyển custom domain nếu có. Đừng xóa dự án cũ trước khi kiểm tra xong.

## Xem thử ở máy Mac

Chạy `python3 scripts/build.py`, rồi mở `dist/index.html` hoặc `dist/bai-viet/index.html`.

## File ZIP khác

File `DHK_Cloudflare_Thu_Cong.zip` là bản website dựng sẵn để tải lên Cloudflare bằng Direct Upload, nhưng **đăng bài mới cần chạy lại build**. Để tự động cập nhật, hãy dùng Git integration và repository này.

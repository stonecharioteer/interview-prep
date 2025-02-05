#[allow(unused)]

fn binary_search(array: &[i32], find: i32) -> isize {
    let mut left = 0;
    let mut right = array.len() as isize - 1;
    while left <= right {
        let mid = left + (right - left) / 2;
        if array[mid as usize] > find {
            right = mid - 1;
        } else if array[mid as usize] < find {
            left = mid + 1;
        } else {
            return mid;
        }
    }
    -1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_binary_search() {
        let array = vec![0, 1, 2, 3, 4, 5, 6, 77];
        assert_eq!(binary_search(&array, 77), 7);
        let array2 = vec![22, 41, 55, 1001, 12354];
        assert_eq!(binary_search(&array2, 0), -1 as isize);
    }
}

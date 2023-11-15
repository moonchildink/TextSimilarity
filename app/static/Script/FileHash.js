/**
 * 通过计算文件HASH值的方法判断文件是否相同，这样可以避免相同文件占用服务器资源
 */

async function calculateFileHash(file) {
    return new Promise((res, rej) => {
        const reader = new FileReader();

        reader.onload = function (e) {
            const buffer = e.target.result;
            crypto.subtle.digest('SHA-256', buffer).then(hashBuffer => {
                const hashArray = Array.from(new Uint8Array(hashBuffer));
                const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
                res(hashHex);
            }).catch(rej);
        };
        reader.onerror = rej;

        reader.readAsArrayBuffer(file);
    });
}

function areFileEqual(file1, file2, callback) {
    Promise.all([calculateFileHash(file1), calculateFileHash(file2)])
        .then(([hash1, hash2]) => {
            const areEqual = hash1 === hash2;
            callback(areEqual);
        })
        .catch(error=>{
            console.error('Error calculating file hash:',error);
            callback(false);
        });
}